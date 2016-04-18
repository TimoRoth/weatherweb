from weatherweb.database import *


def import_mesaurement(station: Station, data):
    for line in data:
        mes = Measurement(datetime=line[0], station=station)
        db.session.add(mes)

        for sensor in station.sensors:
            pos = sensor.position
            if pos < 1 or pos >= len(line):
                continue
            else:
                if line[pos].startswith("?"):
                    continue
                else:
                    data = line[pos]

            mesdata = MeasurementData(measurement=mes, sensor=sensor, data=data)
            db.session.add(mesdata)
