import os

from flask import Flask
from flask_cachecontrol import FlaskCacheControl
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)

app.config.from_object("weatherweb.default_config")
if os.environ.get("WEATHERWEB_SETTINGS") is not None:
    app.config.from_envvar("WEATHERWEB_SETTINGS")

db = SQLAlchemy(app)
cache_control = FlaskCacheControl(app)

import weatherweb.database
import weatherweb.assets
import weatherweb.views
