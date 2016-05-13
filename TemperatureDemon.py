#!/usr/bin/env python
# -*- coding: utf-8 -*-
'''
  My temp demon application
'''

# Import
import os
#from __future__ import division
import time
import sys
import socket
import requests
from datetime import datetime
from DatabaseModel import insert, insertp, inserth

# Globals
version = "1.2"
place = 'Nowhere'

def get_all_temp_page(server) :
    import fcntl

    file = 'static/all'
    f = open(file,'w+')
    try:
        fcntl.flock(f, fcntl.LOCK_EX | fcntl.LOCK_NB)
    except:
        f.close()
        print 'File locked return'
        return False

    url = 'http://'+ server + ':8805/all/'
    try:
        r = requests.get(url, timeout=60)
        page = r.text
    except:
        page = 'Server did not reply'

    f.write(page.encode('utf-8'))

    # Unlock
    fcntl.flock(f, fcntl.LOCK_UN)
    f.close()
    return True

def get_server_temp(server) :
    global place
    if ping_server(server) == False: return 'null'

    url = 'http://'+ server + ':8805/j/'
    try:
        r = requests.get(url, timeout=2)
        d = r.json()
    except:
        d =  {'temp': 'null', 'date' : '0000-00-00 00:00:00' , 'place': 'Unknown', 'sensor': 'null', 'server':url}

    if d['temp'] == 'null': return 'null'
    if d['temp'] == '85.0': return 'null'
    if d['temp'] == '85.00': return 'null'
    d['server'] = server
    timestamp = datetime.strftime(datetime.now(), '%Y-%m-%d %H:%M:%S')
    insert(d['temp'], timestamp, d['place'], sensor=d['sensor'], server=server )
    place = d['place']
    return d['temp']

def get_server_pres(server) :
    if ping_server(server) == False: return 'null'
    url = 'http://'+ server + ':8805/jp/'
    try:
        r = requests.get(url, timeout=2)
        d = r.json()
    except:
        d =  {'pres': 'null', 'date' : '0000-00-00 00:00:00' , 'place': 'Unknown', 'sensor': 'null', 'server':url}

    if d['pres'] == 'null': return 'null'
    d['server'] = server
    timestamp = datetime.strftime(datetime.now(), '%Y-%m-%d %H:%M:%S')
    insertp(d['pres'], timestamp, d['place'], sensor=d['sensor'], server=server )
    return d['pres']

def get_server_humi(server) :
    if ping_server(server) == False: return 'null'
    url = 'http://'+ server + ':8805/jh/'
    try:
        r = requests.get(url, timeout=2)
        d = r.json()
    except:
        d =  {'humi': 'null', 'date' : '0000-00-00 00:00:00' , 'place': 'Unknown', 'sensor': 'null', 'server':url}

    if d['humi'] == 'null': return 'null'
    d['server'] = server
    timestamp = datetime.strftime(datetime.now(), '%Y-%m-%d %H:%M:%S')
    inserth(d['humi'], timestamp, d['place'], sensor=d['sensor'], server=server )
    return d['humi']

def get_random_values():
    tt = random.uniform(10.5, 20.9)
    t = str(round(tt, 2))
    pp = random.uniform(900.5, 1020.9)
    p = str(round(pp, 2))
    hh = random.uniform(12, 99.9)
    h = str(round(hh, 2))
    return (t, p, h)

def ping_server(host) :
    cmd = 'ping -W 1 -c 1 %s > /dev/null 2>&1' % server
    return os.system(cmd) == 0

def blinkled(n, chip) :
    if chip:
        cmd = "/usr/sbin/i2cset -f -y 0 0x34 0x93 %d"
    else:
        cmd = "echo %d >/sys/class/leds/led0/brightness"
    while (n > 0) :
        os.system(cmd % 1)
        time.sleep(1)
        os.system(cmd % 0)
        time.sleep(1)
        n -= 1

def domoticz(url, port, idx, temp):
    urlib = '%s:%s/json.htm?type=command&param=udevice&idx=%s&nvalue=0&svalue=%s' % (url, port, idx, temp)
    try:
        r = requests.get(urlib, timeout=2)
        ok = r.json()
    except:
        return 'Error getting status'

    if ok['status'] != 'OK':
        return 'Status NOT UPDATED'
    else:
        return 'Status UPDATED OK'

def writemypid(pidfile):
    pid = str(os.getpid())
    with file(pidfile, 'w') as f:
        f.write(pid)
    f.close

if __name__ == '__main__':

    import argparse
    parser = argparse.ArgumentParser()
    parser.add_argument('--server', action="store", default='localhost')
    parser.add_argument('--stage', action="store", default="production")
    parser.add_argument('--database', action="store", default="database.db")
    parser.add_argument('--root', action="store", default=".")
    parser.add_argument('--pid', action="store", default="tempdemon.pid")
    parser.add_argument('--broker', action="store", default='http://zerver2.ypketron.tk')
    parser.add_argument('--idx', action="store", default='0' )
    # Boolean
    parser.add_argument('--debug', action="store_true", default=False)
    parser.add_argument('--domoticz', action="store_true", default=False)
    parser.add_argument('--rand', action="store_true", default=False)
    parser.add_argument('--chip', action="store_true", default=False)
    parser.add_argument('--blink', action="store_true", default=False)
    parser.add_argument('--sensehat', action="store_true", default=False)
    parser.add_argument('--roadcast', action="store_true", default=False)
    parser.add_argument('--mqtt', action="store_true", default=False)
    parser.add_argument('--all', action="store_true", default=False)

    # get args
    args = parser.parse_args()

    # Where to start, what to get
    os.chdir(os.path.abspath(args.root))
    current_dir = os.path.dirname(os.path.abspath(__file__))

    # Get and insert into DB
    server = args.server
    t =  get_server_temp(server)

    # Get and insert into DB
    p =  get_server_pres(server)

    # Get and insert into DB
    h =  get_server_humi(server)

    if args.rand:
        import random
        timestamp = datetime.strftime(datetime.now(), '%Y-%m-%d %H:%M:%S')
        t, p, h = get_random_values()
        insert (t, timestamp, place, sensor='fake', server=server)
        insertp(p, timestamp, place, sensor='fake', server=server)
        inserth(h, timestamp, place, sensor='fake', server=server)

    if args.roadcast:
        url = 'http://et:Tre@roadcast.ypketron.tk/ins'
        params = {'value':t,'genre':'temperature', 'hdr':0}
        r = requests.post(url, data = params, timeout=2)

    if args.domoticz and args.idx != 0:
        domoticz(args.url, args.port, args.idx, temp)

    # Blink the led on board
    if args.blink:
       blinkled(4, args.chip)

    if args.all:
        get_all_temp_page('localhost')

    if args.mqtt:
        import paho.mqtt.client as mqtt
        mqttc = mqtt.Client(place)
        mqttc.connect('broker.ypketron.tk', 1883)
        mqttc.publish('Temperature/%s' % place, t)
        mqttc.loop(2) # timeout = 2s

    print (u'Temperature %s°' % t)
    print (u'Pressure %s' % p)
    print (u'Humidity %s' % h)

