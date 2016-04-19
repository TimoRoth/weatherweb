from datetime import date, datetime, timedelta
from pydl15 import DL15


dl = DL15(verbose=True)

dl.connect_telnet("134.102.87.169")

dl.power_on()

res = dl.get_data(since=datetime(year=2016, month=4, day=19, hour=15, minute=40), use_yield=True)

for r in res:
    print(r)

dl.power_off()
dl.close()
