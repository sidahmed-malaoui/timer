#!/usr/bin/python3

import os
try:
    import notify2
except ImportError:
    import pip
    print("Installing missing packages (this will be done the first time only) :")
    if os.getuid() == 0:
        pip.main(['install', 'notify2'])
    else:
        pip.main(['install', 'notify2', '--user'])
    print("Done.\nRerun the command now.")
    exit(0)
import argparse
import re
import time


def timer(total_secs):
    while total_secs >= 0:
        s = total_secs % 60
        m = ((total_secs - s) % 3600)//60
        h = (total_secs - m*60)//3600
        print( "\r\033[k{:02}:{:02}:{:02}".format(h, m, s), end='')
        total_secs -= 1
        time.sleep(1)


def main():
    args_parser = argparse.ArgumentParser(description='This is a timer.')
    args_parser.add_argument('time', type=str, help='time can be just seconds, or of the format hh:mm:ss or mm:ss')

    args = args_parser.parse_args()
    
    # If the time is of the format hh:mm:ss
    if re.search(r"^\d\d?:\d\d?:\d\d?$", args.time):
        h, m, s = args.time.split(':')
        timer(int(h)*3600 + int(m)*60 + int(s))
    # If the time is of the format mm:ss
    elif re.search(r"^\d\d?:\d\d?$", args.time):
        m, s = args.time.split(':')
        timer(int(m)*60 + int(s))
    # If the time is just seconds (a number).
    elif re.search(r"^\d+$", args.time):
        timer(int(args.time))
    else:
        print("Unknown time format : {}".format(args.time))
        exit(-1)

    print()
    # Send the notification.
    notify2.init("timer")
    notification = notify2.Notification("timer", message="end of the specified time {}".format(args.time))
    notification.show()

if __name__ == "__main__":
    main()