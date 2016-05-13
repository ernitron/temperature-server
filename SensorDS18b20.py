#!/usr/bin/env python
# -*- coding: utf-8 -*-

# Import
import subprocess
import os.path
import glob
from DatabaseModel import getplace_db, setplace_db

class Sensor :
    def __init__(self) :
        self.sensor_id = "unknown"
        self.total_count = 0
        base_dir = '/sys/bus/w1/devices/'
        try:
            device_folder = glob.glob(base_dir + '28*')[0]
        except:
            device_folder = '/tmp'

        pos = device_folder.rfind('-')
        if pos > 0:
           self.sensor_id = device_folder[pos+1:]
        self.device_file = device_folder + '/w1_slave'

        if os.path.isfile(self.device_file) :
            print self.device_file
        else:
            self.device_file = "/dev/null"

        self.place = self.readplacename()
        try:
            from sense_hat import SenseHat
            self.sensehat = SenseHat()
	except:
            self.sensehat = None

    def reinit(self) :
        '''
        On Raspberry PI (wheezy)
        Warning for DS18B20P (parasite) it is necessary:
        1. Add to /boot/config.txt the following line:
        dtoverlay=w1-gpio,pullup="y"
        2. Modprobe with:
        # sudo modprobe w1_gpio pullup=1
        # sudo modprobe w1_therm strong_pullup=1 (or =2)

        1-Wire Default reading is on GPIO 4
        '''

        os.system('modprobe w1-gpio pullup=1')
        os.system('modprobe w1-therm strong_pullup=1')

        self.__init__()

    def sensorid(self) :
        return self.sensor_id

    def total_count(self) :
        return self.total_count

    def placename(self):
        return self.place

    def setplacename(self, name):
        self.place = setplace_db(name)

    def readplacename(self):
        self.place = getplace_db()
        return self.place

    def read_temp(self):
        if os.path.isfile(self.device_file) == False:
            return 'null'

        with open(self.device_file, 'r') as f:
            lines = f.readlines()
        f.close()

        try:
            equals_pos = lines[1].find('t=')
            if equals_pos != -1:
              # The first two characters are "t=", so get rid of those and convert the temperature from a string to a number.
              # Put the decimal point in the right place and display it.
              temp_string = lines[1][equals_pos+2:]
              temp = float(temp_string) / 1000.0
              #temp_f = temp * 9.0 / 5.0 + 32.0 # Fahreneit
              temp = str(round(temp, 2))
        except:
            temp = 'null'

        self.total_count += 1
        return temp

    def read_pressure(self):
        if self.sensehat != None:
            p = self.sensehat.get_pressure()
            p = round(p, 2)
        else:
            p = 'null'
        self.total_count += 1
        return p

    def read_humidity(self):
        if self.sensehat != None:
            h = self.sensehat.get_humidity()
            h = round(h, 2)
        else:
            h = 'null'
        self.total_count += 1
        return h

    def sensordebug(self):
        sysdev = '/sys/bus/w1/devices/'
        h = '<h2>Listing %s</h2>' % sysdev
        if os.path.isfile(self.device_file):
            h += self.device_file

        h += '''<pre>
        On Raspberry PI (wheezy and probably jeanny don't work)
        Warning for DS18B20P (parasite) it is necessary:
        1. Add to /boot/config.txt the following line:
        dtoverlay=w1-gpio,pullup="y"
        2. Modprobe with:
        # sudo modprobe w1_gpio pullup=1
        # sudo modprobe w1_therm strong_pullup=1 (or =2)

        1-Wire Default reading is on GPIO 4
        </pre>
        '''

        h += '''
<pre>
Sensor Database:
28-000007011a5f DS18B20
28-0000073e313a DS18B20

28-000007011953 DS18B20 PAR
28-00000740146b DS18B20 PAR
28-0000073ade97 DS18B20 PAR
28-0000073ae2ec DS18B20 PAR
28-000007013e91 DS18B20 PAR
28-0000070118c5 DS18B20 PAR
</pre>'''

        subprocess.Popen(["nohup", "pkill", "modprobe"])

        return h
