import csv
from datetime import datetime
from plumbum import cli


class Loader(cli.Application):
    input_file = cli.SwitchAttr(["i", "intput"], help="File with mac's")
    output_file = cli.SwitchAttr(["o", "output"], help="Write data to file")
    observation = cli.SwitchAttr(["O", "observation"],
                                 default=120,
                                 help="Duration of observation in seconds")
    verbose = cli.Flag(["v", "verbose"])

    def main(self):
        self.macs: dict = {}
        self.table: list = []

        self._load_from_file()
        self._read_mac_time()
        self._calculate_time()

    def _load_from_file(self):
        with open(self.input_file, 'r') as mac:
            reader = csv.reader(mac)
            self.table = list(reader)

    def _read_mac_time(self):
        for line in self.table:
            mac = line[0]

            # 2020-01-07 14:03:13
            time_fmt = '%Y-%m-%d %H:%M:%S'
            try:
                start_time = datetime.strptime(line[1].strip(), time_fmt)
                end_time = datetime.strptime(line[2].strip(), time_fmt)
            except ValueError:
                print(line)
                pass

            times = (start_time, end_time - start_time)
            if mac in self.macs:
                self.macs[mac].append(times)
            else:
                self.macs[mac] = [times]

    def _calculate_time(self):
        skipped =  open("skipped", 'w')
        with open(self.output_file, 'w') as output:
            for key, all_times in self.macs.items():
                if 'DA:A1:19' in key:
                    skipped.write("%s\n" % key)
                    if all_times:
                        skipped.write('start: %s, duration: %ss\n' %
                            (all_times[0][0], all_times[0][1].total_seconds()))
                    continue

                if len(all_times) < 5:
                    continue

                if len(all_times) > 1:
                    first_t = all_times[0]
                elif len(all_times) == 1:
                    line = ('%s\nstart: %s, duration: %ss\n' %
                            (key, all_times[0][0], all_times[0][1].total_seconds()))
                    if self.verbose:
                        print(line, end='')
                    output.write(line)
                else:
                    continue

                calculated_time = {}
                curr_t = first_t

                for i, times in enumerate(all_times):
                    if i == len(all_times)-1:
                        continue

                    next_t = all_times[i+1]
                    total = (next_t[0] - all_times[i][0]).total_seconds()
                    if total < int(self.observation):
                        if curr_t in calculated_time:
                            if total == 0:
                                calculated_time[curr_t] += 60
                            else:
                                calculated_time[curr_t] += total
                        else:
                            calculated_time[curr_t] = 60
                    else:
                        curr_t = all_times[i]

                if len(all_times) > 2:
                    if self.verbose:
                        print(key)
                    output.write(key)
                for time, times in calculated_time.items():
                    if times < float(self.observation):
                        output.write("#remove\n")
                        break
                    if len(all_times) > 2:
                        line = ('\nstart: %s, duration: %ss\n' % (time[0], times))
                        if self.verbose:
                            print(line, end='')
                        output.write(line)
        skipped.close()


if __name__ == "__main__":
    Loader.run()
