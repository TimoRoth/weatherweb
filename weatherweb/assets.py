from flask_assets import Environment, Bundle
from . import app


assets = Environment(app)

default_js = Bundle("jquery.js", filters="jsmin", output="gen/charts.js")
charts_js = Bundle("jquery.js", "highcharts.js", filters="jsmin", output="gen/packed_charts.js")
css_all = Bundle("style.css", filters="cssmin", output="gen/packed.css")

assets.register("default_js", default_js)
assets.register("charts_js", charts_js)
assets.register("css_all", css_all)
