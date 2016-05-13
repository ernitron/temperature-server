#!/usr/bin/env python
# -*- coding: utf-8 -*-

from peewee import *

'''
# -------------------- DATABASE --------------------------------
# CREATE TABLE Temperature(id integer primary key autoincrement, temp float, timestamp text, location text );
# CREATE TABLE Pressure(id integer primary key autoincrement, press float, timestamp text, location text );
# CREATE TABLE Humidity(id integer primary key autoincrement, humi float, timestamp text, location text );
'''

database = 'database.db'

db = SqliteDatabase(database)

def Connect():
    global db
    db.connect()

class Temperature(Model):
    temp = FloatField()
    timestamp = DateTimeField()
    location = TextField()
    sensor = TextField()
    server = TextField()

    class Meta:
        database = db # This model uses the "database.db"

class Pressure(Model):
    pressure = FloatField()
    timestamp = DateTimeField()
    location = TextField()
    sensor = TextField()
    server = TextField()

    class Meta:
        database = db # This model uses the "database.db"

class Humidity(Model):
    humidity = FloatField()
    timestamp = DateTimeField()
    location = TextField()
    sensor = TextField()
    server = TextField()

    class Meta:
        database = db # This model uses the "database.db"

def create_db():
    db.create_tables([Temperature, Pressure, Humidity], safe=True)
    insert(temp='85.0', timestamp='2016-04-05 00:00:00', location='MyPlace', sensor='None', server='None')

def getplace_db():
    i = Temperature.select().order_by(Temperature.id.desc()).get()
    return i.location

def setplace_db(location):
    i = Temperature.select().order_by(Temperature.id.desc()).get()
    i.location = location
    i.save()
    return location

def insert(temp, timestamp, location, server='', sensor=''):
    if temp == 'null' : return
    ret = Temperature.create(temp=temp, timestamp=timestamp, location=location, sensor=sensor, server=server)
    return ret

def insertp(pressure, timestamp, location, server='', sensor=''):
    if pressure == 'null' : return
    ret = Pressure.create(pressure=pressure, timestamp=timestamp, location=location, sensor=sensor, server=server)
    return ret

def inserth(humidity, timestamp, location, server='', sensor=''):
    if humidity == 'null' : return
    ret = Humidity.create(humidity=humidity, timestamp=timestamp, location=location, sensor=sensor, server=server)
    return ret

def read_value_from_db(n) :
    sql = "SELECT id,temp,timestamp from (select id,temp,timestamp from Temperature where id > 1 order by id DESC limit %d) order by id asc" %n
    rows = Temperature.raw(sql)
    return rows

def read_press_from_db(n) :
    sql = "SELECT id,pressure,timestamp FROM (SELECT id,pressure,timestamp from Pressure where id > 1 order by id DESC limit %d) order by id asc" %n
    rows = Pressure.raw(sql)
    return rows

def read_humi_from_db(n) :
    sql = "SELECT id,humidity,timestamp FROM (SELECT id,humidity,timestamp from Humidity where id > 1 order by id DESC limit %d) order by id asc" %n
    rows = Humidity.raw(sql)
    return rows

def read_value_from_db_orm(n) :
    rows = Temperature.select().order_by(Temperature.id.desc()).limit(n)
    return rows

def gettemp(id) :
    row = Temperature.get(Temperature.id == id)
    return row

def listtemps() :
    rows = Temperature.select().order_by(Temperature.timestamp.desc())
    return rows

def delete(id) :
    t = Temperature.get(Temperature.id == id)
    ret = t.delete_instance()  # Returns the number of rows deleted.
    return ret

def filter_data(n) :
    first = True
    for r in read_value_from_db_orm(int(n)) :
        if first == False and abs(old - r.temp) > 2.5:
           delete(r.id)
        first = False
        old = r.temp

    first = True
    for r in read_press_from_db(int(n)) :
        if first == False and abs(old - r.pressure) > 20.0:
           t = Pressure.get(Pressure.id == r.id)
           t.delete_instance()  # Returns the number of rows deleted.
        first = False
        old = r.pressure

    first = True
    for r in read_humi_from_db(int(n)) :
        if first == False and abs(old - r.humidity) > 9.0:
           t = Humidity.get(Humidity.id == r.id)
           t.delete_instance()  # Returns the number of rows deleted.
        first = False
        old = r.humidity


def userdatabase(user) :
    usersuffix = '.' + user
    database = database.replace('.db', usersuffix)

    if not os.path.isfile(database):
        return None
    return database

if __name__ == '__main__':
    import os
    os.system('rm ' + database)
    create_db()



