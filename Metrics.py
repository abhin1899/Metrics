from subprocess import Popen, PIPE


class SystemMetrics:

    def __init__(self, pid):
        self.pid = pid
        self.metric_rates = {
            'read_bytes' : 0,
            'write_bytes' : 0
        }

    def cpu_mem_usage(self):
        p = Popen("top -p " + str(self.pid) + " -b -n 1 |grep " + str(self.pid) + " | awk '{print $9,$10}'", shell=True,
                  stdout=PIPE, stderr=PIPE)
        out, err = p.communicate()
        cpu = str(out.split()[0])
        mem = str(out.split()[1])
        return cpu, mem

    def disk_speed(self):
        p = Popen("sudo iotop -p " + str(self.pid) + " -b -n 1 | grep " + str(self.pid) + " | awk '{print $4,$6}'", shell=True,
                  stdout=PIPE, stderr=PIPE)
        out, err = p.communicate()
        disk_read = out.split()[0]
        disk_write = out.split()[1]
        return disk_read, disk_write

    def io_usage(self):
        p = Popen("cat /proc/" + str(self.pid) + "/io | awk 'BEGIN{r=0;w=0} /^rchar*/ {r= $2};/^write_bytes*/ {w= $2} END{ print r,w}'",
                  shell=True, stdout=PIPE, stderr=PIPE)
        out, err = p.communicate()
        read_bytes = int(out.split()[0])
        write_bytes = int(out.split()[1])
        return read_bytes, write_bytes

    def get_read_write_rate(self):
        read_rate = 0; write_rate = 0
        read_bytes, write_bytes = self.io_usage()
        if self.metric_rates['read_bytes'] == 0:
            self.metric_rates['read_bytes'] = read_bytes
        else:
            read_rate = read_bytes - self.metric_rates['read_bytes']
            self.metric_rates['read_bytes'] = read_bytes
        if self.metric_rates['write_bytes'] == 0:
            self.metric_rates['write_bytes'] = write_bytes
        else:
            write_rate = write_bytes - self.metric_rates['write_bytes']
            self.metric_rates['write_bytes'] = write_bytes
        return read_rate, write_rate
