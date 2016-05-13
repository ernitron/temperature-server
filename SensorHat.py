#!/usr/bin/env python
# -*- coding: utf-8 -*-

# Import
import subprocess
import os.path

from DatabaseModel import getplace_db, setplace_db
from sense_hat import SenseHat

class Sensor :
    def __init__(self) :
        self.sensor_id = "sensor hat"
        self.fileplace = 'tempplace.conf'
        self.total_count = 0
        self.device_file = "/dev/null"
        self.sense = SenseHat()
        self.place = self.readplacename()

    def reinit(self) :
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
        temp = "null"
        tt = self.sense.get_temperature()
        th = self.sense.get_temperature_from_humidity()
        tf = self.sense.get_temperature_from_pressure()

        tf = float(tt)
        tf = tf - 10.0 # Fattore di correzione
        tt = round(tt, 2)
        tc = round(tf, 2)
        th = round(th, 2)
        tf = round(tf, 2)

        self.total_count += 1
        return str(tc)

    def read_pressure(self):
        p = self.sense.get_pressure()
        p = round(p, 2)
        self.total_count += 1
        return str(p)

    def read_humidity(self):
        h = self.sense.get_humidity()
        h = round(h, 2)
        self.total_count += 1
        return str(h)

    def sensordebug(self):
        return 'Sense Hat'
