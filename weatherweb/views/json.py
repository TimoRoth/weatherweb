from flask import Response, jsonify, request
from flask_cachecontrol import cache_for
from datetime import datetime, timedelta
import tzlocal
import pytz
import math

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
@app.route("/json/sensor_data/<int:sensor_id>/since/<int:since>")
@app.route("/json/sensor_data/<int:sensor_id>/since/<int:since>/until/<int:until>")
@cache_for(minutes=5)
def sensor_data(sensor_id, start=0, start_mult=0, count=-1, since=-1, until=-1, latest=False):
    res = []

    sensor = Sensor.query.get(sensor_id)

    if sensor is None:
        return jsonify({"error": "Sensor not found"})

    station = sensor.station
    tz = pytz.timezone(station.timezone)

    sdata = MeasurementData.query.join(MeasurementData.measurement).filter(MeasurementData.sensor_id == sensor_id)
    sdata = sdata.options(db.contains_eager(MeasurementData.measurement))

    dt = None

    if since >= 0:
        dt = datetime.fromtimestamp(since)
        dt = dt.astimezone(tz)
        dt = dt.replace(tzinfo=None, microsecond=0)
        sdata = sdata.filter(Measurement.datetime >= dt)
    elif start_mult < 0:  # Today
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

    if until >= 0:
        dt = datetime.fromtimestamp(until)
        dt = dt.astimezone(tz)
        dt = dt.replace(tzinfo=None, microsecond=0)
        sdata = sdata.filter(Measurement.datetime <= dt)
    elif count >= 0 and dt is not None:
        dt = dt + timedelta(hours=start_mult * count)
        sdata = sdata.filter(Measurement.datetime <= dt)

    if latest:
        sdata = sdata.order_by(Measurement.datetime.desc()).limit(1)
    else:
        sdata = sdata.order_by(Measurement.datetime.asc())

    sdata = sdata.all()

    if request.args.get("hourly_avg") is not None:
        sdata = hourly_avg(sensor, tz, sdata)
    else:
        sdata = convert_data(tz, sdata)

    if sensor.group == "rain":
        unit = "mm/%smin" % station.mes_duration
    else:
        unit = sensor.unit

    for data in sdata:
        if data is None:
            continue
        dt = data["datetime"]
        if request.args.get("human") is not None:
            res.append([str(dt), data["data"]])
        else:
            res.append([int(dt.timestamp()) * 1000, data["data"]])

    return jsonify({
        "data": res,
        "aux": {
            "sensor_id": sensor.id,
            "sensor_name": sensor.name,
            "station_name": station.name,
            "station_location": station.location,
            "station_timezone": station.timezone,
            "unit": unit,
        }
    })


def calc_avg(sensor, data, dt):
    if sensor.group == "wind":
        rad = [math.radians(d) - math.pi for d in data]
        sx = sum([math.cos(r) for r in rad])
        sy = sum([math.sin(r) for r in rad])
        res = math.degrees(math.atan2(sy, sx) + math.pi)
    else:
        res = float(sum(data))/len(data)

    return {
        "datetime": dt,
        "data": res
    }


def hourly_avg(sensor, tz, sdata):
    col = []
    col_dt = None
    for data in sdata:
        dt = tz.localize(data.measurement.datetime)

        if col_dt is None:
            col_dt = dt

        if dt.hour == col_dt.hour:
            col.append(data.data)
        else:
            yield calc_avg(sensor, col, col_dt)
            col_dt = dt
            col = [data.data]

    if col_dt is not None:
        yield calc_avg(sensor, col, col_dt)


def convert_data(tz, sdata):
    for data in sdata:
        yield {"datetime": tz.localize(data.measurement.datetime), "data": data.data}
