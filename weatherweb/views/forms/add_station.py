from flask_wtf import Form
from wtforms import StringField, IntegerField
from wtforms.validators import DataRequired


class AddStationForm(Form):
    name = StringField("Name", validators=[DataRequired()])
    location = StringField("Location")
    address = StringField("Address")
    timezone = IntegerField("Timezone", validators=[DataRequired()], default="CET")
