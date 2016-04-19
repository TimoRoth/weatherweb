from flask import Response, jsonify

from weatherweb import app
from weatherweb.database import *


@app.route("/json/list_stations")
def list_stations():
    res = []

    for station in Station.query.options(db.subqueryload(Station.sensors)).all():
        sensors = []
        for sensor in station.sensors:
            sensors.append({
                "id": sensor.id,
                "name": sensor.name,
                "comment:": sensor.comment,
                "unit": sensor.unit,
                "position": sensor.position
            })
        res.append({
            "id": station.id,
            "name": station.name,
            "location": station.location,
            "address": station.address,
            "utc_offset": station.utc_offset,
            "sensors": sensors
        })

    return jsonify({"stations": res})


@app.route("/json/station_measurements/<station_id>")
def station_measurements(station_id):
    res = []

    station = Station.query\
        .options(db.joinedload(Station.measurements).subqueryload(Measurement.data), db.joinedload(Station.sensors))\
        .filter(Station.id == station_id)\
        .first()

    if station is None:
        return "{}"

    for mes in station.measurements:
        sensor_data = {}

        for mesdata in mes.data:
            sensor_data[mesdata.sensor.id] = mesdata.data

        res.append({
            "datetime": str(mes.datetime),
            "sensor_data": sensor_data
        })

    return jsonify({"measurements": res})


@app.route("/json/sensor_data/<sensor_id>")
def sensor_data(sensor_id):
    res = []

    sensor = Sensor.query\
        .options(db.subqueryload(Sensor.data).subqueryload(MeasurementData.measurement))\
        .get(sensor_id)

    for data in sensor.data:
        # res.append([int(data.measurement.datetime.timestamp()) * 1000, data.data])
        res.append([data.measurement.datetime, data.data])

    return jsonify({"data": res})
