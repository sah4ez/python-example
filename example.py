import csv
from datetime import datetime

with open('./ttt', 'r') as f:
    READER = csv.reader(f)
    TABLE = list(READER)

macs: dict = {}
for line in TABLE:
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

    if len(all_times) > 1:
        first_t = all_times[0]
    elif len(all_times) == 1:
        print(('start: %s, duration: %ss' % (all_times[0][0], all_times[0][1].total_seconds())))
    else:
        continue

    calculated_time = {}
    curr_t = first_t

    for i, times in enumerate(all_times):
        if i == len(all_times)-1:
            continue

        next_t = all_times[i+1]
        total = (next_t[0] - all_times[i][0]).total_seconds()
        if total < 120:
            if curr_t in calculated_time:
                calculated_time[curr_t] += total
            else:
                calculated_time[curr_t] = 0
        else:
            curr_t = all_times[i]

    for t in calculated_time:
        times = calculated_time[t]
        print(('start: %s, duration: %ss' % (t[0], times)))
