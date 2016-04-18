import sys

from sqlalchemy.exc import SQLAlchemyError
from flask import render_template, url_for, request, Response

from weatherweb import app
from weatherweb.database import *
from weatherweb.utils.auth import requires_auth
from weatherweb.utils.list_routes import list_routes
from weatherweb.utils.pydl15.parse import parse as parse_dl15
from weatherweb.utils.measurements import import_mesaurement


@app.route("/admin/")
@requires_auth
def admin():
    items = []

    for r in list_routes():
        if "/admin/" not in r["url"]:
            continue
        item = {
            "name": r["endpoint"],
            "href": r["url"],
        }
        items.append(item)

    return render_template("admin_landing.html", admin_items=items)


@app.route("/admin/add_station")
@requires_auth
def add_station():
    return "Test"


@app.route("/admin/init_db")
@requires_auth
def init_db():
    try:
        db.create_all()
    except SQLAlchemyError:
        return sys.exc_info()[0]
    return "OK"


@app.route("/admin/manual_feed", methods=['GET'])
@requires_auth
def manual_feed():
    stations = [{
        "name": "Automatic",
        "location": "Automatic",
        "id": -1
    }]

    for station in Station.query.all():
        stations.append({
            "name": station.name,
            "location": station.location,
            "id": station.id,
        })

    return render_template("admin_manual_feed.html", stations=stations)


@app.route("/admin/manual_feed", methods=['POST'])
@requires_auth
def manual_feed_data():
    name, data = parse_dl15(request.form["data"])
    station_id = int(request.form["station"])

    if station_id == -1:
        stations = Station.query.filter(Station.name == name).all()
        if len(stations) > 1:
            return "Station name not unique, autodetection failed."
        elif len(stations) <= 0:
            return "Station not found!"
        station = stations[0]
    else:
        station = Station.query.filter(Station.id == station_id).first()

    if station is None:
        return "Station not found!"

    import_mesaurement(station, data)

    db.session.commit()

    return station.location
