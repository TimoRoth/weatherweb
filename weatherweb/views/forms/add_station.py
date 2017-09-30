from flask_wtf import FlaskForm
from wtforms import StringField, IntegerField, BooleanField
from wtforms.validators import DataRequired


class AddStationForm(FlaskForm):
    name = StringField("Name", validators=[DataRequired()])
    location = StringField("Location")
    address = StringField("Address")
    timezone = StringField("Timezone", validators=[DataRequired()], default="Etc/UTC")
    mes_duration = IntegerField("Measurement Duration", validators=[DataRequired()], default=10)
    ext_duration = IntegerField("Extreme Duration", validators=[DataRequired()], default=30)
