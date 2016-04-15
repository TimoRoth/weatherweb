from apscheduler.schedulers.background import BackgroundScheduler
from weatherweb import app
import weatherweb.database as db


@app.before_first_request
def init_cron():
    sched = BackgroundScheduler()
    sched.start()

    sched.add_job(fetchdata, 'interval', minutes=10)
    fetchdata()


def fetchdata():
    with app.app_context():
        pass
