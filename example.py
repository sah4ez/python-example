import csv
from datetime import datetime

with open('./ttt', 'r') as f:
    reader = csv.reader(f)
    table = list(reader)

macs: dict = {}
for line in table:
    mac = line[0]
    # 2020-01-07 14:03:13
    time_fmt = '%Y-%m-%d %H:%M:%S'
    start_time = datetime.strptime(line[1].strip(), time_fmt)
    end_time = datetime.strptime(line[2].strip(), time_fmt)

    times = (start_time, end_time - start_time)
    if mac not in macs:
        macs[mac] = [times]
    else:
        all_times = macs[mac]
        all_times.append(times)

for key in macs:
    print(key)
    all_times = macs[key]
    for times in all_times:
        print(times[0], times[1])
