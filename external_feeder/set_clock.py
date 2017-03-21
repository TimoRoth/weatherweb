#!/usr/bin/env python3
from pydl15 import DL15
from os import system

dl15 = DL15(True)
dl15.connect_serial("/dev/ttyFTDI")

dl15.power_on()

dl15.get_date()
dl15.get_time()
system("date")

dl15.set_clock()

dl15.get_status()
system("date")

dl15.power_off()
dl15.close()
