from flask import Response, jsonify
import pytz

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
            "timezone": station.timezone,
            "is_dst": station.is_dst,
            "sensors": sensors
        })

    return jsonify({"stations": res})


@app.route("/json/sensor_data/<sensor_id>")
def sensor_data(sensor_id):
    res = []

    sensor = Sensor.query\
        .options(db.subqueryload(Sensor.data).joinedload(MeasurementData.measurement))\
        .get(sensor_id)
    station = sensor.station

    tz = pytz.timezone(station.timezone)

    for data in sensor.data:
        dt = tz.localize(data.measurement.datetime, is_dst=station.is_dst)
        res.append([dt.timestamp() * 1000, data.data])

    return jsonify({"data": res})
