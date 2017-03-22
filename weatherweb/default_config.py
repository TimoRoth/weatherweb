from werkzeug.security import generate_password_hash

SQLALCHEMY_TRACK_MODIFICATIONS = False
SQLALCHEMY_DATABASE_URI = 'mysql+mysqlconnector://timo:IFzOUgjWcLYcFSK26pPW@klima.uni-bremen.de/weatherweb'
SQLALCHEMY_ECHO = True

ADMIN_USER = "admin"
ADMIN_PASS = generate_password_hash("1234")

WTF_CSRF_ENABLED = True
SECRET_KEY = 'sdf846wejipafe6r7e7SRTG'

GLOBAL_TITLE = "WeatherWeb"

TEMPLATES_AUTO_RELOAD = True
