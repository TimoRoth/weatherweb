from flask import request

from .. import app
from ..database import *
from ..utils.measurements import import_measurement
from ..utils.pydl15.parse import parse_dl15


@app.route("/ext/last_data/<int:station_id>")
def last_data(station_id):
    mes = Measurement.query.filter(Measurement.station_id == station_id).order_by(Measurement.datetime.desc()).first()
    if mes is None:
        return "Station not found", 404
    return mes.datetime.strftime("%Y-%m-%d %H:%M:%S")


@app.route("/ext/feed/<int:station_id>", methods=["POST", "GET"])
@app.route("/ext/feed/<int:station_id>/<auth_string>", methods=["POST", "GET"])
def feed_data(station_id, auth_string=None):
    station = Station.query.filter(Station.id == station_id).first()
    if station is None:
        return "Station not found", 404
    if not station.address.startswith("ext"):
        return "Not an external station", 403

    if station.address.startswith("extauth:"):
        auth = station.address[8:]
        if auth != auth_string:
            return "Invalid auth", 403
    else:
        ext = station.address[4:]
        if ext != request.remote_addr:
            return "Invalid auth", 403

    if request.method == "GET":
        data = request.args.get("data")
    else:
        data = request.form["data"]

    if data is None:
        return "No data"

    name, data = parse_dl15(data)
    cnt = import_measurement(station, data)

    return "Imported %d lines of data" % cnt


@app.route("/ext/feed_cr/<int:station_id>/<auth_string>", methods=["PUT"])
def feed_cr(station_id, auth_string):
    with open("/tmp/put_data.txt", "wb") as f:
        f.write(request.data)
    return "OK"
