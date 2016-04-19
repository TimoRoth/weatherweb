from werkzeug.security import check_password_hash
from functools import wraps
from flask import request, Response
from .. import app


def check_auth(user, passwd):
    return user == app.config['ADMIN_USER'] and check_password_hash(app.config['ADMIN_PASS'], passwd)


def authenticate():
    return Response("Login required", 401, {"WWW-Authenticate": "Basic realm=\"Login Required\""})


def requires_auth(f):
    @wraps(f)
    def d(*args, **kwargs):
        auth = request.authorization
        if not auth or not check_auth(auth.username, auth.password):
            return authenticate()
        return f(*args, **kwargs)
    return d
