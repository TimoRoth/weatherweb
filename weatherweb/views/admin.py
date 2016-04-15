from weatherweb import app
from weatherweb.database import *
from weatherweb.utils.auth import requires_auth


@app.route("/admin/")
@requires_auth
def admin():
    return "YAY"
