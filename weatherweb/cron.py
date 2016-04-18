from datetime import datetime

from apscheduler.schedulers.background import BackgroundScheduler
from weatherweb import app
from weatherweb.database import *


def init_cron():
    sched = BackgroundScheduler()
    sched.start()

    sched.add_job(fetchdata, "interval", minutes=10)
    sched.add_job(fetchdata)


def fetchdata():
    with app.app_context():
        pass
