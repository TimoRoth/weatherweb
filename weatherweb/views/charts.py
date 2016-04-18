from weatherweb import app


@app.route("/")
def index():
    return ""