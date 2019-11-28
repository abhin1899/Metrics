import argparse
import time
import signal
import datetime
from Metrics import SystemMetrics
# from FileHandler import LocalFileHandler
import logging, logging.handlers
import time
import csv


def create_parser():
    parser = argparse.ArgumentParser()
    parser.add_argument('pid', help='pid of Any process')
    parser.add_argument('-o', '--output-file', help='Define path of output .csv file')
    return parser


if __name__ == '__main__':
    args = create_parser().parse_args()
    
    #server_url = args.server_url if args.server_url else '127.0.0.1'
    output_file = args.output_file if args.output_file else './output.csv'
    pid = args.pid
    sm = SystemMetrics(pid)
    # TODO: Change later
    cores = '2'

    output = list()
    output.append(['TimeStamp','Cores','CPU_Utilization','Memory_Utilization','IO_Read_Rate',
        'IO_Write_Rate','Read Latency','Write Latency'
    ])

# Signal handler to stop the program
    def sig_handler(signal, frame):
        del output[1]   # Remove first row as it is an outlier

        # # Store locally
        # lfh = LocalFileHandler(output_file)
        # lfh.write_to_csv(output)

        # Store on S3
        #sfh = logging.FileHandler(output_file)
        #sfh.write_to_csv(output)
        with open(output_file, "wb") as f:
            writer = csv.writer(f)
            writer.writerows(output)
        print(output)
        exit()

    signal.signal(signal.SIGINT, sig_handler)

    while True:
        print '.'
        cpu = 0; mem = 0;
        read_latency_rate = 0; write_latency_rate = 0
        read_bytes_rate = 0; write_bytes_rate = 0
        tst=[]
        ts=time.time()
        st=datetime.datetime.fromtimestamp(ts).strftime('%H:%M:%S')
        tst.append(str(st))


        try:
            cpu, mem = sm.cpu_mem_usage()
            read_bytes_rate, write_bytes_rate = sm.get_read_write_rate()
        except IndexError:
            # TODO: Handle gracefully
            print('IndexError (Mostly ending)')

        output.append(tst  + [cores, cpu, mem, read_bytes_rate, write_bytes_rate, read_latency_rate, write_latency_rate])
        time.sleep(0.5)
