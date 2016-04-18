from flask.ext.assets import Environment, Bundle
from weatherweb import app


assets = Environment(app)

charts_js = Bundle("highcharts.src.js", filters="jsmin", output="gen/packed.js")
assets.register("charts_js", charts_js)