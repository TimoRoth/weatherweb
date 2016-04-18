from .. import app
from flask import url_for


def list_routes():
    res = []
    for rule in app.url_map.iter_rules():
        if "GET" not in rule.methods:
            continue
        opts = {}
        for arg in rule.arguments:
            opts[arg] = "[%s]" % arg
        url = url_for(rule.endpoint, **opts)
        res.append({"url": url, "endpoint": rule.endpoint})
    return res
