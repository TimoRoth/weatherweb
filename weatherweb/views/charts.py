from flask import render_template, url_for, request, Response

from .. import app
from ..database import *


@app.route("/test")
def test_chart():
    return render_template("base_chart.html")


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

    return render_template("temp_and_rain_chart.html", hours=hours, station=station, temp_sensors=temp_sensors, rain_sensors=rain_sensors, since=since, until=until)


@app.route("/charts/show_sensor/<int:sensor_id>")
@app.route("/charts/show_sensor/<int:sensor_id>/last_hours/<int:hours>")
@app.route("/charts/show_sensor/<int:sensor_id>/since/<int:since>")
@app.route("/charts/show_sensor/<int:sensor_id>/since/<int:since>/until/<int:until>")
def show_sensor(sensor_id, hours=48, since=-1, until=-1):
    sensor = Sensor.query.get(sensor_id)

    if sensor is None:
        return "Sensor not found!"

    return render_template("single_sensor.html", hours=hours, sensor=sensor, since=since, until=until)
