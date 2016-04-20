from .. import app
from flask import url_for


def list_simple_routes():
    res = []
    for rule in app.url_map.iter_rules():
        if "GET" not in rule.methods:
            continue
        if len(rule.arguments) > 0:
            continue
        url = url_for(rule.endpoint)
        res.append({"url": url, "endpoint": rule.endpoint})
    return res
