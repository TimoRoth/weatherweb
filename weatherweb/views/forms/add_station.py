from flask_wtf import Form
from wtforms import StringField, IntegerField, BooleanField
from wtforms.validators import DataRequired


class AddStationForm(Form):
    name = StringField("Name", validators=[DataRequired()])
    location = StringField("Location")
    address = StringField("Address")
    timezone = StringField("Timezone", validators=[DataRequired()], default="Etc/GMT-1")
