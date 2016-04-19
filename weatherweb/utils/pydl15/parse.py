from datetime import datetime


def fixup_datetime(fields):
    # Fixup midnight being 24 instead of 00
    if fields[-1][:3] == "24:":
        fields[-1] = "00" + fields[-1][2:]

    dt = " ".join(fields[-2:])
    dt = datetime.strptime(dt, "%d.%m.%y %H:%M")
    fields = fields[0:-2]
    fields[0] = dt
    return fields


def parse(data):
    if isinstance(data, str):
        data = [x for x in data.split("\n") if x.strip()]
    res = []
    res_name = ""
    for line in data:
        line = line.strip()
        fields = [f for f in line.split(" ") if f]
        if line.startswith("END"):
            if len(fields) < 4:
                res_name = "Unknown"
            else:
                res_name = fields[3]
        else:
            fields = fixup_datetime(fields)
            res.append(fields)
    return res_name, res
