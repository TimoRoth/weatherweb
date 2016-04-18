from datetime import date

from weatherweb.utils.pydl15 import DL15

dl = DL15(verbose=True)

device = DL15.query_serial_device()
dl.connect_serial(device)
# dl.connect_telnet("134.102.87.169")

dl.power_on()

res = dl.get_data(day=date.today())
# res = dl.get_current_data_human()

for r in res:
    print(r)

dl.power_off()
dl.close()
