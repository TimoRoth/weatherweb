import sys

from sqlalchemy.exc import SQLAlchemyError
from flask import render_template, flash, url_for, request, Response, redirect

from .. import app
from ..database import *
from ..utils.auth import requires_auth
from ..utils.list_routes import list_routes
from ..utils.pydl15.parse import parse_dl15
from ..utils.measurements import import_measurement
from ..cron import do_fetch

from .forms import AddStationForm, AddSensorForm, ManualFeedForm
from .forms import get_station_choices


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


@app.route("/admin/add_station", methods=["GET", "POST"])
@requires_auth
def add_station():
    form = AddStationForm()

    if form.is_submitted():
        if form.validate():
            sta = Station()
            sta.name = form.name.data
            sta.location = form.location.data
            sta.address = form.address.data
            sta.timezone = form.timezone.data
            sta.is_dst = form.is_dst.data
            db.session.add(sta)
            db.session.commit()

            flash("Created station %s with ID %s" % (form.name.data, sta.id))
            return redirect(url_for("admin"))
        else:
            flash("Form validation failed!")
            flash(form.errors)

    return render_template("generic_form.html", form=form, form_dest="add_station", title="Add Station")


@app.route("/admin/add_sensor", methods=["GET", "POST"])
@requires_auth
def add_sensor():
    form = AddSensorForm()
    form.station.choices = get_station_choices(with_auto=False)

    if form.validate_on_submit():
        sta = Station.query.get(form.station.data)

        if sta is None:
            flash("Station %s not found!" % form.station.data)
            return redirect(url_for("admin"))

        sen = Sensor()

        sen.name = form.name.data
        sen.comment = form.comment.data
        sen.unit = form.unit.data
        sen.position = form.position.data
        sen.station = sta

        db.session.add(sen)
        db.session.commit()

        flash("Sensor #%s added to station #%s on position %s!" % (sen.id, sta.id, sen.position))

        form.position.raw_data = None
        form.position.data = sen.position + 1

    return render_template("generic_form.html", form=form, form_dest="add_sensor", title="Add Sensor")


@app.route("/admin/init_db")
@requires_auth
def init_db():
    try:
        db.create_all()
        flash("Successfully initialized database")
    except SQLAlchemyError:
        flash(sys.exc_info()[0])
    return redirect(url_for("admin"))


@app.route("/admin/manual_feed", methods=["GET", "POST"])
@requires_auth
def manual_feed():
    form = ManualFeedForm()
    form.station.choices = get_station_choices()

    if form.validate_on_submit():
        try:
            name, data = parse_dl15(form.station_data.data)
            station_id = form.station.data

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

            cnt = import_measurement(station, data)
            db.session.commit()

            flash("Successfully imported %s data lines!" % cnt)
            return redirect(url_for("admin"))
        except:
            db.session.rollback()
            raise

    return render_template("generic_form.html", form=form, form_dest="manual_feed", title="Manual Data Upload")


@app.route("/admin/trigger_fetch")
@requires_auth
def trigger_fetch():
    do_fetch()
    flash("Fetch done")
    return redirect(url_for("admin"))
