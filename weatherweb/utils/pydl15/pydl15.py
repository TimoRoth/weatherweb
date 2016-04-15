from datetime import datetime
import struct
import time
import sys


class DL15:
    def __init__(self, verbose=False):
        self.port = None
        self.tn = None
        self.tn_timeout = 30
        self.ser_timeout = 2
        self.verbose = verbose

    def _log(self, c):
        if self.verbose:
            print(c)

    @staticmethod
    def query_serial_device():
        import serial.tools.list_ports

        ports = []
        for port in serial.tools.list_ports.comports():
            print("%s: %s" % (len(ports), port))
            ports.append(port.device)
        if len(ports) == 1:
            device = ports[0]
            print("Auto-Selected only available device")
        else:
            try:
                i = int(input("Select port index: "))
            except ValueError:
                print("Not a number")
                sys.exit(-1)
            if i < 0 or i >= len(ports):
                print("Invalid index!")
                sys.exit(-1)
            device = ports[i]
        return device

    def connect_serial(self, device):
        import serial

        self._log("Opening serial port %s ..." % device)
        self.port = serial.Serial(device, baudrate=9600,
                                  bytesize=serial.SEVENBITS, parity=serial.PARITY_EVEN, stopbits=serial.STOPBITS_ONE,
                                  xonxoff=True, timeout=self.ser_timeout)
        self._log("Success!")

    def connect_telnet(self, address, port=23):
        import telnetlib

        self._log("Connecting to %s:%s ..." % (address, port))
        self.tn = telnetlib.Telnet(host=address, port=port, timeout=self.tn_timeout)
        self._log("Connected!")

    def close(self):
        if self.port is not None:
            self.port.close()
        if self.tn is not None:
            self.tn.close()

    def send_raw(self, b):
        if self.tn is not None:
            self.tn.write(b)
        else:
            self.port.write(b)

    def readline(self):
        if self.port is not None:
            line = self.port.readline()
        elif self.tn is not None:
            line = self.tn.read_until(b"\n", timeout=self.tn_timeout)
        else:
            line = b""
        self._log("GOT LINE: %s" % line)
        line = line.decode("ascii")
        return line

    def power_on(self):
        self._log("POWER ON")
        self.send_raw(b"\x00\n")
        time.sleep(1)

    def send_command(self, cmd):
        b = "\x02%s\x03\n" % str(cmd)
        b = b.encode("ascii")
        self._log("SEND COMMAND '%s'" % cmd)
        self.send_raw(b)

    def readlines(self, count=-1):
        lines = []
        while count != 0:
            count -= 1
            line = self.readline()
            if line:
                lines.append(line.rstrip())
            if not line or line.lstrip()[:3] == "END":
                break
        return lines

    def power_off(self):
        self.send_command("PD")

    def set_clock(self, dt=None):
        if dt is None:
            print("Waiting for full minute...")
            dt = datetime.now()
            dif = 60 - dt.second
            if dif == 60:
                pass
            elif dif > 25:
                self.power_off()
                time.sleep(dif - 2)
                self.power_on()
            while True:
                dt = datetime.now()
                if dt.second == 0:
                    break
                time.sleep(0.25)
        self.send_command("ZM%s" % dt.minute)
        self.readlines(3)
        self.send_command("ZH%s" % dt.hour)
        self.readlines(3)
        self.send_command("DT%s" % dt.day)
        self.readlines(3)
        self.send_command("DM%s" % dt.month)
        self.readlines(3)
        self.send_command("DJ%s" % (dt.year % 100))
        self.readlines(3)

    def get_all_data(self):
        self.send_command("GS")
        return self.readlines()

    @staticmethod
    def _encode_since(dt):
        d = dt.day + 28
        mo = dt.month + 28
        y = (dt.year % 100) + 28
        h = dt.hour + 28
        m = dt.minute + 28
        return struct.pack("BBBBB", d, mo, y, h, m)

    @staticmethod
    def _encode_day(dt):
        d = dt.day + 28
        mo = dt.month + 28
        y = (dt.year % 100) + 28
        return struct.pack("BBB", d, mo, y)

    def get_data(self, since=None, day=None):
        if since is not None:
            cmd = b"\x02ds" + self._encode_since(since) + b"\x03\n"
            self._log("GET DATA SINCE %s.%s.%s %s:%s" %
                      (since.day, since.month, since.year, since.hour, since.minute))
        elif day is not None:
            cmd = b"\x02ts" + self._encode_day(day) + b"\x03\n"
            self._log("GET DATA ON DAY %s.%s.%s" % (day.day, day.month, day.year))
        else:
            cmd = b"\x02SS\x03\n"
            self._log("GET DATA")
        self.send_raw(cmd)
        return self.readlines()

    def get_extremes(self, since=None, day=None):
        if since is not None:
            cmd = b"\x02de" + self._encode_since(since) + b"\x03\n"
            self._log("GET EXTREMES SINCE %s.%s.%s %s:%s" %
                      (since.day, since.month, since.year, since.hour, since.minute))
        elif day is not None:
            cmd = b"\x02te" + self._encode_day(day) + b"\x03\n"
            self._log("GET EXTREMES ON DAY %s.%s.%s" % (day.day, day.month, day.year))
        else:
            cmd = b"\x02EE\x03\n"
            self._log("GET EXTREMES")
        self.send_raw(cmd)
        return self.readlines()

    def get_current_data(self):
        self.send_command("mm")
        return self.readlines(1)

    def get_current_data_human(self):
        self.send_command("MM")
        return self.readlines()

    def get_status(self):
        self.send_command("LL")
        return self.readlines()

    def get_version(self):
        self.send_command("XX")
        return self.readlines(1)

    def get_date(self):
        self.send_command("DD")
        return self.readlines(2)

    def get_time(self):
        self.send_command("ZZ")
        return self.readlines(2)

    def get_help(self):
        self.send_command("HH")
        return self.readlines()

    def cancel(self):
        self.send_raw(b"\x04\n")