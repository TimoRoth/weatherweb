from werkzeug.security import generate_password_hash

SQLALCHEMY_TRACK_MODIFICATIONS = False
SQLALCHEMY_DATABASE_URI = 'sqlite:///default.sqlite'
SQLALCHEMY_ECHO = True

ADMIN_USER = "admin"
ADMIN_PASS = generate_password_hash("1234")

GLOBAL_TITLE = "WeatherWeb"
