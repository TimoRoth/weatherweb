from htmlmin.main import minify
from flask_assets import Environment, Bundle
from . import app


assets = Environment(app)

default_js = Bundle("jquery.js", filters="jsmin", output="gen/charts.js")
charts_js = Bundle("jquery.js",
                   "highcharts.js",
                   "highcharts-exporting.js",
                   "highcharts-export-data.js",
                   "highcharts-accessibility.js",
                   filters="jsmin", output="gen/packed_charts.js")
charts_js_src = Bundle("jquery.src.js",
                       "highcharts.src.js",
                       "highcharts-exporting.src.js",
                       "highcharts-export-data.src.js",
                       "highcharts-accessibility.src.js",
                       output="gen/packed_charts_src.js")
css_all = Bundle("style.css", filters="cssmin", output="gen/packed.css")

assets.register("default_js", default_js)
assets.register("charts_js", charts_js_src)
assets.register("css_all", css_all)


@app.after_request
def minify_html(resp):
    if resp.content_type == u'text/html; charset=utf-8':
        resp.set_data(minify(resp.get_data(as_text=True)))
    return resp
