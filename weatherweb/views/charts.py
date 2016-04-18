from flask import render_template, url_for, request, Response

from weatherweb import app


@app.route("/")
def index():
    return render_template("base_chart.html")