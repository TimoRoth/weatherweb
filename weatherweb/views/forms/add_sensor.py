from flask_wtf import Form
from wtforms import StringField, SelectField, IntegerField
from wtforms.validators import DataRequired

from .manual_feed import get_station_choices


class AddSensorForm(Form):
    station = SelectField("Station", validators=[DataRequired()], coerce=int, choices=[(-2, "Unset")])
    name = StringField("Name", validators=[DataRequired()])
    comment = StringField("Comment")
    unit = StringField("Unit", validators=[DataRequired()], default="°C")
    position = IntegerField("Position", validators=[DataRequired()], default=1)

