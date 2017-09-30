from datetime import datetime, timedelta
from flask_script import Manager
import threading
import csv

from . import app
from .database import *
from .utils.pydl15.pydl15 import DL15
from .utils.pydl15.parse import parse_dl15_gen
from .utils.measurements import import_dl15_measurement, import_toa5_measurement


manager = Manager(app)


def handle_dl15(station: Station, dl15: DL15):
    dl15.power_on()
    mes = Measurement.query.filter(Measurement.station_id == station.id).order_by(Measurement.datetime.desc()).first()
    if mes is None:
        data = dl15.get_data(use_yield=True)
    else:
        data = dl15.get_data(since=mes.datetime + timedelta(minutes=1), use_yield=True)

    print("Importing data from station %s" % station.name)
    res = parse_dl15_gen(data)
    cnt = import_dl15_measurement(station, res)
    print("Imported %s data lines for Station %s" % (cnt, station.name))

    dl15.power_off()
    dl15.close()


def handle_toa5(station: Station, toahandle):
    reader = csv.reader(toahandle, delimiter=",", quoting=csv.QUOTE_NONNUMERIC, skipinitialspace=True)

    header = next(reader)
    if header[0] != "TOA5":
        raise RuntimeError("Invalid TOA5 header")

    var_names = next(reader)
    unit_names = next(reader)
    val_type = next(reader)

    if len(var_names) != len(unit_names) or len(var_names) != len(val_type):
        raise RuntimeError("Header lengths mismatch")

    print("Importing data from station %s" % station.name)
    cnt = import_toa5_measurement(station, var_names, reader)
    print("Imported %s data lines for Station %s" % (cnt, station.name))


@manager.command
def fetchdata():
    """Fetch data from all registered stations"""

    with app.app_context():
        for station in Station.query.all():
            adr = str(station.address).strip()
            if adr.startswith("tcp:"):
                adr = adr[4:]
                port = 23
                if ":" in adr:
                    i = adr.index(":")
                    try:
                        port = int(adr[i+1:])
                    except ValueError:
                        port = 23
                    adr = adr[:i]
                dl15 = DL15()
                try:
                    dl15.connect_telnet(adr, port)
                    handle_dl15(station, dl15)
                except:
                    continue
            elif adr.startswith("ser:"):
                adr = adr[4:]
                dl15 = DL15()
                try:
                    dl15.connect_serial(adr)
                    handle_dl15(station, dl15)
                except:
                    continue
            elif adr.startswith("toa5:"):
                adr = adr[5:]
                with open(adr, newline="") as toafile:
                    try:
                        handle_toa5(station, toafile)
                    except Exception as e:
                        print("Error parsing TOA5: %s" % repr(e))
                        continue
            else:
                continue


def do_fetch():
    t = threading.Thread(target=fetchdata)
    t.start()


@manager.command
def init_db():
    """Initialize database"""
    app.config["SQLALCHEMY_ECHO"] = True
    db.create_all()


def run_manager():
    return manager.run()
