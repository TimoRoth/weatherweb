from flask_wtf import FlaskForm
from wtforms import StringField, SelectField, IntegerField
from wtforms.validators import DataRequired

from .manual_feed import get_station_choices


class AddSensorForm(FlaskForm):
    station = SelectField("Station", validators=[DataRequired()], coerce=int, choices=[(-2, "Unset")])
    name = StringField("Name", validators=[DataRequired()])
    comment = StringField("Comment")
    unit = StringField("Unit", validators=[DataRequired()], default="°C")
    group = StringField("Group")
    position = IntegerField("Position", default=0)
    sensor_name = StringField("Sensor Variable Name")
