#!/usr/bin/env python3

from subprocess import Popen, PIPE
from datetime import datetime
from itertools import repeat
from sys import exit, exc_info
from re import split, search, MULTILINE
from time import sleep

def exec_command(command):
    proc = Popen(command, stdout=PIPE, stderr=PIPE)
    try:
        out, err = proc.communicate(15)
    except TimeoutExpired:
        proc.kill()
        out, err = proc.communicate()
    return out

def battery():
    command = ["cat", "/sys/class/power_supply/BAT0/capacity"]
    status = exec_command(command)
    bat_per = str(status.decode()).strip()
    power_s = get_power_supply()
    return '{0} : {1}%'.format(power_s, bat_per)

def get_power_supply():
    command = ["cat", "/sys/class/power_supply/AC/online"]
    status = exec_command(command)
    if '1' in status.decode():
        return 'AC'
    else:
        return 'Battery'

def fdate():
    return datetime.now().strftime('%a %d/%m/%y %H:%M')

def diskspace():
    command = ["df", "-h", "|", "grep", "'/$'"]
    return exec_command(command).decode()

def network():
    inet_p  = r'(?<=inet )([0-9]{1,3}\.){3}[0-9]{1,3}'
    iface_p = r'^\w+:(?! <LOOP)'
    split_p = r'^[0-9]+: '
    command = ['ip', 'addr']
    status = exec_command(command).decode()
    data = split(split_p, status, maxsplit=0, flags=MULTILINE)

    for d in data:
        try:
            status = '{0}{1}'.format(search(iface_p, d).group(),
                    search(inet_p, d, MULTILINE).group())
        except AttributeError:
            status = 'No Active Interface'
        except:
            print('{} occurred...'.format(exc_info()[0]))
            exit(1)
    return status

if __name__ == "__main__":
    while True:
        data = [diskspace(), network(), fdate()]
        exec_command(['xsetroot', '-name', ' | '.join(data)])
        sleep(20)
