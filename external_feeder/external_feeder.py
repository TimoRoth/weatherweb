#!/usr/bin/env python3
from pydl15 import DL15
from datetime import datetime, timedelta
import sys
import requests

STATION_ID = "1"
APP_URL = "https://klima.uni-bremen.de/"
AUTH = None

if AUTH is not None:
    AUTH = "/" + AUTH
if APP_URL.endswith("/"):
    APP_URL = APP_URL[:-1]

res = requests.get("%s/ext/last_data/%s" % (APP_URL, STATION_ID))
if res.status_code != 200:
    print("Getting last_data date failed with HTTP error %s" % res.status_code)
    sys.exit(1)

since_date = datetime.strptime(res.text, "%Y-%m-%d %H:%M:%S") + timedelta(minutes=1)
print("Uploading data since %s" % since_date)

dl15 = DL15()
dl15.connect_serial("/dev/ttyFTDI")

dl15.power_on()
data = dl15.get_data(since=since_date)
dl15.power_off()
dl15.close()

data = [x.strip() for x in data if x.strip()]
data = "\n".join(data)

print(data)
sys.exit(0)

res = requests.post("%s/ext/feed/%s%s" % (APP_URL, STATION_ID, AUTH if AUTH is not None else ""), data={'data': data})
print(res.text)

if res.status_code != 200:
    sys.exit(2)
