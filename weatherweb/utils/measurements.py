from sqlalchemy.exc import IntegrityError
from datetime import datetime
from ..database import *
import math


def import_dl15_measurement(station: Station, data):
    count = 0

    station_id = station.id
    sensors = [(s.id, s.position) for s in station.sensors]
    db.session.flush()

    for line in data:
        try:
            mes = Measurement(datetime=line[0], station_id=station_id)
            db.session.add(mes)
            db.session.flush()
            mesdata = []

            for sensor in sensors:
                pos = sensor[1]
                if pos < 1 or pos >= len(line):
                    data = float("nan")
                else:
                    if line[pos].startswith("?"):
                        data = None
                    else:
                        data = line[pos]

                mesdata.append(dict(measurement_id=mes.id, sensor_id=sensor[0], data=data))

            db.session.bulk_insert_mappings(MeasurementData, mesdata)
            db.session.commit()
            count += 1
        except IntegrityError:
            db.session.rollback()
            continue

    return count


def import_toa5_measurement(station: Station, var_names, data):
    count = 0

    station_id = station.id
    sensors = dict()
    for s in station.sensors:
        sensors[s.sensor_name] = s.id
    unused_vars = dict()
    db.session.flush()

    for line in data:
        if len(line) != len(var_names):
            raise RuntimeError("Mesurement line length mismatches")
        try:
            dt = datetime.strptime(line[0], "%Y-%m-%d %H:%M:%S")
            mes = Measurement(datetime=dt, station_id=station_id, record_number=int(line[1]))
            db.session.add(mes)
            db.session.flush()

            sens_values = zip(var_names[2:], line[2:])
            mesdata = []
            for vals in sens_values:
                if vals[0] not in sensors:
                    unused_vars[vals[0]] = True
                    continue
                sens_id = sensors[vals[0]]
                data = float(vals[1])
                if math.isnan(data):
                    data = None
                mesdata.append(dict(measurement_id=mes.id, sensor_id=sens_id, data=data))

            db.session.bulk_insert_mappings(MeasurementData, mesdata)
            db.session.commit()
            count += 1
        except IntegrityError:
            db.session.rollback()

    print("Unused data variables: %s" % repr(unused_vars))

    return count
