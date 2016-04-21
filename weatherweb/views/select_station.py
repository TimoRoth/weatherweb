from flask import render_template, url_for, request, Response

from .. import app
from ..database import *


@app.route("/")
def index():
    stations = Station.query.all()
    return render_template("select_station.html", stations=stations)

@app.route("/show_station/<int:id>")
def show_station(id):
    station = Station.query.get(id)

    if station is None:
        return "Station not found"

    return render_template("show_station.html", station=station)
