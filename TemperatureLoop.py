#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
import time
from sense_hat import SenseHat

debug = False

def mainloop(internal_url, external_url, scroll_speed):
    sense = SenseHat()
    sense.set_rotation(270)
    url_i = 'http://%s:8805/j' % internal_url
    url_e = 'http://%s:8805/j' % external_url
    while True:
        t = sense.get_temperature()
        p = sense.get_pressure()
        h = sense.get_humidity()
        th = sense.get_temperature_from_humidity()
        tf = sense.get_temperature_from_pressure()

        t = round(t, 2)
        tc = round(t - 7.5, 2) # Correction factor = 9.0
        th = round(th, 2)
        tf = round(tf, 2)
        p = round(p, 2)
        h = round(h, 2)

        # External
        d = getjtemp(url_i)
        temp_i = d['temp']

        # Internal from chip1
        d = getjtemp(url_e)
        temp_e = d['temp']

        if debug:
            msg = u"Int=%s°, Ext=%s°, T=%s° (correct %s), P=%s Pa, H=%s %%" % (temp_i, temp_e, t, tc, p, h)
            print(msg)

        msg = u"%s" % (temp_i)
        sense.show_message(msg, scroll_speed=scroll_speed, text_colour=[188,128,52])
        time.sleep(2)

        msg = u"%s" % (temp_e)
        sense.show_message(msg, scroll_speed=scroll_speed, text_colour=[0,0,250])
        time.sleep(2)

        # Pressure
        msg = u"%s" % (p)
        sense.show_message(msg, scroll_speed=scroll_speed, text_colour=[0,80,0])
        time.sleep(2)

        # Humidity
        msg = u"%s" % (h)
        sense.show_message(msg, scroll_speed=scroll_speed, text_colour=[0,0,80])
        time.sleep(2)

    # until infinite

def getjtemp(url):
    import requests
    try:
        r = requests.get(url, timeout=2)
        data = r.json()
    except:
        data =  {'temp':'nil', 'date':'0000-00-00 00:00:00', 'place':'Unknown', 'sensor':'nil', 'server':url}
    return data

def writemypid(pidfile):
    pid = str(os.getpid())
    with file(pidfile, 'w') as f:
        f.write(pid)
    f.close

if __name__ == '__main__':
    import argparse
    parser = argparse.ArgumentParser()
    parser.add_argument('--external', action="store", default="localhost")
    parser.add_argument('--internal', action="store", default="chip1.ypketron.tk")
    parser.add_argument('--speed', action="store", default="0.1")
    parser.add_argument('--root', action="store", default=".")
    parser.add_argument('--pid', action="store", default="/tmp/temploop.pid")
    parser.add_argument('--debug', action="store_true", default=False)

    args = parser.parse_args()

    # Write pid
    writemypid(args.pid)

    # Where to start, what to get
    root = os.path.abspath(args.root)
    os.chdir(root)
    current_dir = os.path.dirname(os.path.abspath(__file__))

    debug = args.debug
    speed = float(args.speed)
    mainloop(args.internal, args.external, speed)
