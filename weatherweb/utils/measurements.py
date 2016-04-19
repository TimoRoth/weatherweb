from sqlalchemy.exc import IntegrityError
from ..database import *
from datetime import datetime, timedelta
import pytz


def import_measurement(station: Station, data):
    count = 0

    station_id = station.id
    sensors = [(s.id, s.position) for s in station.sensors]
    db.session.flush()

    tz = pytz.timezone(station.timezone)

    for line in data:
        try:
            mes = Measurement(datetime=tz.localize(line[0], is_dst=False), station_id=station_id)
            db.session.add(mes)
            db.session.flush()
            mesdata = []

            for sensor in sensors:
                pos = sensor[1]
                if pos < 1 or pos >= len(line):
                    data = float("nan")
                else:
                    if line[pos].startswith("?"):
                        data = float("nan")
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
