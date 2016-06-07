from datetime import datetime, timedelta
from flask_script import Manager
import threading

from . import app
from .database import *
from .utils.pydl15.pydl15 import DL15
from .utils.pydl15.parse import parse_dl15_gen
from .utils.measurements import import_measurement


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
    cnt = import_measurement(station, res)
    print("Imported %s data lines for Station %s" % (cnt, station.name))

    dl15.power_off()
    dl15.close()


@manager.command
def fetchdata():
    """Fetch data from all registered stations"""

    with app.app_context():
        for station in Station.query.all():
            adr = str(station.address)
            adr = adr.lower().strip()
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
                except:
                    continue
            elif adr.startswith("ser:"):
                adr = adr[4:]
                dl15 = DL15()
                try:
                    dl15.connect_serial(adr)
                except:
                    continue
            else:
                continue
            try:
                handle_dl15(station, dl15)
            except:
                pass


def do_fetch():
    t = threading.Thread(target=fetchdata)
    t.start()


@manager.command
def init_db():
    """Initialize database"""
    app.config["SQLALCHEMY_ECHO"] = True
    db.create_all()


def run_manager():
    manager.run()
