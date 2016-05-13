#!/usr/bin/env python
# -*- coding: utf-8 -*-

# Import
import subprocess
import os.path
import glob

class Sensor :

    def __init__(self) :

        self.sensorid = "sensor unknown"
        self.fileplace = 'tempplace.conf'
        self.place = 'Unknown place'
        self.total_count = 0

        base_dir = '/sys/bus/w1/devices/'
        try:
            device_folder = glob.glob(base_dir + '28*')[0]
        except:
            device_folder = '/tmp'

        pos = device_folder.rfind('-')
        if pos > 0:
           self.sensorid = device_folder[pos+1:]
        self.device_file = device_folder + '/w1_slave'

        if os.path.isfile(self.device_file) :
            print self.device_file
        else:
            self.device_file = "/dev/null"

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
        return self.sensorid

    def total_count(self) :
        return self.total_count

    def setplacename(self, name):
        with open(self.fileplace, "w") as f:
           f.write(name)
        f.close()
        self.place = name

    def placename(self):
        self.place = "Temp"
        with open(self.fileplace, 'r') as f:
            lines = f.readlines()
        f.close()
        self.place = lines[0]
        return self.place

    def read_temp(self):
        temp = "null"

        with open(self.device_file, 'r') as f:
             lines = f.readlines()
        f.close()

        try:
            equals_pos = lines[1].find('t=')
        except:
            equals_pos = -1

        if equals_pos != -1:
             # The first two characters are "t=", so get rid of those and convert the temperature from a string to a number.
             # Put the decimal point in the right place and display it.
             temp_string = lines[1][equals_pos+2:]
             temp = float(temp_string) / 1000.0
             #temp_f = temp * 9.0 / 5.0 + 32.0 # Fahreneit
             temp = str(round(temp, 2))

        self.total_count += 1
        return temp

    def read_pressure(self):
        self.total_count += 1
        return 'null'

    def read_humidity(self):
        self.total_count += 1
        return 'null'

    def sensordebug(self):
        sysdev = '/sys/bus/w1/devices/'
        proc = subprocess.Popen('ls -l %s' % sysdev, shell=True, stdout=subprocess.PIPE)
        h = '<h2>ls -l %s</h2>' % sysdev
        for line in proc.stdout.readlines():
            h += line

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

        h += '''<pre>
000007011a5f DS18B20
0000073e313a DS18B20

000007011953 DS18B20 PAR
00000740146b DS18B20 PAR
0000073ade97 DS18B20 PAR
        </pre>
        '''

        subprocess.Popen(["nohup", "pkill", "modprobe"])

        return h
