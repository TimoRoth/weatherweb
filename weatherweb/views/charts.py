from flask import render_template, url_for, request, Response

from .. import app
from ..database import *


@app.route("/test")
def test_chart():
    return render_template("base_chart.html")


@app.route("/charts/summary")
@app.route("/charts/summary/last_hours/<int:hours>")
@app.route("/charts/summary/since/<int:since>")
@app.route("/charts/summary/since/<int:since>/until/<int:until>")
def summary(hours=24, since=-1, until=-1):
    wind_speed_sensor = Sensor.query.get(14)
    wind_dir_sensor = Sensor.query.get(3)
    temp_sensor = Sensor.query.get(15)
    humid_sensor = Sensor.query.get(18)
    rain_sensor = Sensor.query.get(12)
    bila_sensor = Sensor.query.get(20)

    dura_unit = "10min"

    if since >= 0:
        kwargs = {"since": since, "until": until}
    elif hours > 5 * 24:
        kwargs = {"start": hours, "start_mult": 1, "hourly_avg": True}
        dura_unit = "h"
    else:
        kwargs = {"start": hours, "start_mult": 1}

    if request.args.get("hourly_avg") is not None:
        kwargs["hourly_avg"] = True

    data_url = url_for("multi_sensor_data",
                       sensor_ids=",".join(map(str, [wind_speed_sensor.id, wind_dir_sensor.id, temp_sensor.id,
                                                     humid_sensor.id, rain_sensor.id, bila_sensor.id])),
                       **kwargs)

    return render_template("summary_chart.html", hours=hours, since=since, until=until, data_url=data_url, dura_unit=dura_unit,
                           wind_speed_sensor=wind_speed_sensor, wind_dir_sensor=wind_dir_sensor, bila_sensor=bila_sensor,
                           temp_sensor=temp_sensor, humid_sensor=humid_sensor, rain_sensor=rain_sensor)


@app.route("/charts/temp_and_rain/<int:station_id>")
@app.route("/charts/temp_and_rain/<int:station_id>/last_hours/<int:hours>")
@app.route("/charts/temp_and_rain/<int:station_id>/since/<int:since>")
@app.route("/charts/temp_and_rain/<int:station_id>/since/<int:since>/until/<int:until>")
def temp_and_rain(station_id, hours=48, since=-1, until=-1):
    station = Station.query.get(station_id)

    if station is None:
        return "Station not found"

    temp_sensors = Sensor.query.filter(Sensor.station == station).filter(Sensor.group == "temp").all()
    rain_sensors = Sensor.query.filter(Sensor.station == station).filter(Sensor.group == "rain").all()

    return render_template("temp_and_rain_chart.html", hours=hours, station=station,
                           temp_sensors=temp_sensors, rain_sensors=rain_sensors,
                           since=since, until=until)


@app.route("/charts/show_sensor/<int:sensor_id>")
@app.route("/charts/show_sensor/<int:sensor_id>/last_hours/<int:hours>")
@app.route("/charts/show_sensor/<int:sensor_id>/since/<int:since>")
@app.route("/charts/show_sensor/<int:sensor_id>/since/<int:since>/until/<int:until>")
def show_sensor(sensor_id, hours=48, since=-1, until=-1):
    sensor = Sensor.query.get(sensor_id)

    if sensor is None:
        return "Sensor not found!"

    return render_template("single_sensor.html", hours=hours, sensor=sensor, since=since, until=until)
