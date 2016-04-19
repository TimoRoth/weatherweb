from flask_wtf import Form
from wtforms import TextAreaField, SelectField
from wtforms.validators import DataRequired

from weatherweb.database import *


def get_station_choices(with_auto=True):
    if with_auto:
        res = [(-1, "Automatic")]
    else:
        res = []

    for station in Station.query.all():
        res.append((station.id, "%s - %s" % (station.name, station.location)))

    return res


class ManualFeedForm(Form):
    station = SelectField("Station", validators=[DataRequired()], coerce=int, choices=[(-2, "Unset")])
    station_data = TextAreaField("Data", validators=[DataRequired()])
