from flask import Response, jsonify, request
from flask.ext.cachecontrol import cache_for
from datetime import datetime, timedelta
import tzlocal
import pytz

from .. import app
from ..database import *


@app.route("/json/list_stations")
@cache_for(hours=12)
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
            "sensors": sensors
        })

    return jsonify({"stations": res})


@app.route("/json/sensor_data/<int:sensor_id>")
@app.route("/json/sensor_data/<int:sensor_id>/latest", defaults={'latest': True})
@app.route("/json/sensor_data/<int:sensor_id>/today", defaults={'start_mult': -1})
@app.route("/json/sensor_data/<int:sensor_id>/last_hours/<int:start>", defaults={'start_mult': 1})
@app.route("/json/sensor_data/<int:sensor_id>/last_days/<int:start>", defaults={'start_mult': 24})
@app.route("/json/sensor_data/<int:sensor_id>/last_weeks/<int:start>", defaults={'start_mult': 168})
@app.route("/json/sensor_data/<int:sensor_id>/last_hours/<int:start>/count/<int:count>", defaults={'start_mult': 1})
@app.route("/json/sensor_data/<int:sensor_id>/last_days/<int:start>/count/<int:count>", defaults={'start_mult': 24})
@app.route("/json/sensor_data/<int:sensor_id>/last_weeks/<int:start>/count/<int:count>", defaults={'start_mult': 168})
@app.route("/json/sensor_data/<int:sensor_id>/start/<int:start>/<int:start_mult>/count/<int:count>")
@cache_for(minutes=5)
def sensor_data(sensor_id, start=0, start_mult=0, count=-1, latest=False):
    res = []

    sensor = Sensor.query.get(sensor_id)

    if sensor is None:
        return jsonify({"error": "Sensor not found"})

    station = sensor.station
    tz = pytz.timezone(station.timezone)

    sdata = MeasurementData.query.join(MeasurementData.measurement).filter(MeasurementData.sensor_id == sensor_id)
    sdata = sdata.options(db.contains_eager(MeasurementData.measurement))

    dt = None

    if start_mult < 0:
        ltz = tzlocal.get_localzone()
        dt = datetime.now(ltz)
        dt = dt.replace(hour=0, minute=0, second=0, microsecond=0)
        dt = dt.astimezone(tz)
        dt = dt.replace(tzinfo=None, microsecond=0)
        sdata = sdata.filter(Measurement.datetime >= dt)
    elif start_mult:
        dt = datetime.now(pytz.utc) - timedelta(hours=start * start_mult)
        dt = dt.astimezone(tz)
        dt = dt.replace(tzinfo=None, microsecond=0)
        sdata = sdata.filter(Measurement.datetime >= dt)

    if count >= 0 and dt is not None:
        dt = dt + timedelta(hours=start_mult * count)
        sdata = sdata.filter(Measurement.datetime <= dt)

    if latest:
        sdata = [sdata.order_by(Measurement.datetime.desc()).first()]
    else:
        sdata = sdata.order_by(Measurement.datetime.asc()).all()

    for data in sdata:
        dt = tz.localize(data.measurement.datetime)
        if request.args.get("human") is not None:
            res.append([str(dt), data.data])
        else:
            res.append([int(dt.timestamp()) * 1000, data.data])

    return jsonify({
        "data": res,
        "aux": {
            "sensor_id": sensor.id,
            "sensor_name": sensor.name,
            "station_name": station.name,
            "station_location": station.location,
            "station_timezone": station.timezone,
            "unit": sensor.unit,
        }
    })
