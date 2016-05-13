#!/usr/bin/env python
# -*- coding: utf-8 -*-
'''
  A temperature/pressure/humidity server application
'''

# Imports
import os
#from __future__ import division
import sys
import cherrypy
from socket import getfqdn as gethostname
from datetime import datetime

# Jinja2 templating
from jinja2 import Environment, FileSystemLoader

# My libraries
from DatabaseModel import read_value_from_db, read_press_from_db, read_humi_from_db, filter_data

# Globals
version = "4.1.4"
uuid='56ty66fa-6kld-8opb-ak29-0t7f5d294686'
device = None
sensor = None

# ------------------------ AUTHENTICATION --------------------------------
from cherrypy.lib import auth_basic

# Tre ;)
users = {'et': 'et'}

def validate_password(self, login, password):
    if login in users :
        if encrypt(password) == users[login] :
            cherrypy.session['username'] = login
            return True

    return False

def encrypt(pw):
    from md5 import md5
    return md5(pw).hexdigest()

# ------------------------ CLASS --------------------------------
class Root:
    @cherrypy.expose
    def index(self, sample='288'):
        temp = sensor.read_temp()
        place = sensor.placename()
        timestamp = datetime.strftime(datetime.now(), '%Y-%m-%d %H:%M:%S')

        data = '['
        for t in read_value_from_db(int(sample)):
            if t.id == 1: continue
            data +=  "{'value': %s, 'date':'%s'}, " % (t.temp, t.timestamp)
        data += ']'

        tmpl = env.get_template('index.html')
        return tmpl.render(footer=footer, place=place, temp=temp, timestamp=timestamp, total_count=sensor.total_count, data=data)

    @cherrypy.expose
    def single(self):
        temp = sensor.read_temp()
        place = sensor.placename()
        timestamp = datetime.strftime(datetime.now(), '%Y-%m-%d %H:%M:%S')

        tmpl = env.get_template('single.html')
        return tmpl.render(footer=footer, place=place, temp=temp, timestamp=timestamp, total_count=sensor.total_count)

    @cherrypy.expose
    def filter(self, sample='288'):
        filter_data(sample)
        return self.index()

    @cherrypy.expose
    def pressure(self, sample='288'):
        pres = sensor.read_pressure()
        place = sensor.placename()
        timestamp = datetime.strftime(datetime.now(), '%Y-%m-%d %H:%M:%S')

        data = '['
        for p in read_press_from_db(int(sample)):
            if p.id == 1: continue
            data +=  "{'value': %s, 'date':'%s'}, " % (p.pressure, p.timestamp)
        data += ']'

        tmpl = env.get_template('pressure.html')
        return tmpl.render(footer=footer, place=place, pres=pres, timestamp=timestamp, total_count=sensor.total_count, data=data)

    @cherrypy.expose
    def humidity(self, sample='288'):
        humi = sensor.read_humidity()
        place = sensor.placename()
        timestamp = datetime.strftime(datetime.now(), '%Y-%m-%d %H:%M:%S')

        data = '['
        for h in read_humi_from_db(int(sample)):
            if h.id == 1: continue
            data +=  "{'value': %s, 'date':'%s'}, " % (h.humidity, h.timestamp)
        data += ']'

        tmpl = env.get_template('humidity.html')
        return tmpl.render(footer=footer, place=place, humi=humi, timestamp=timestamp, total_count=sensor.total_count, data=data)

    @cherrypy.expose
    @cherrypy.tools.json_out()
    def j(self):
        temp = sensor.read_temp()
        place = sensor.placename()
        sensorid = sensor.sensorid()
        d = datetime.strftime(datetime.now(), '%Y-%m-%d %H:%M:%S')
        json =  {'temp':temp, 'date':d, 'place':place, 'sensor':sensorid, 'server':hostname}
        return json

    @cherrypy.expose
    @cherrypy.tools.json_out()
    def jp(self):
        pres = sensor.read_pressure()
        place = sensor.placename()
        sensorid = sensor.sensorid()
        d = datetime.strftime(datetime.now(), '%Y-%m-%d %H:%M:%S')
        json =  {'pres':pres, 'date':d, 'place':place, 'sensor':sensorid, 'server':hostname}
        return json

    @cherrypy.expose
    @cherrypy.tools.json_out()
    def jh(self):
        humi = sensor.read_humidity()
        place = sensor.placename()
        sensorid = sensor.sensorid()
        d = datetime.strftime(datetime.now(), '%Y-%m-%d %H:%M:%S')
        json =  {'humi':humi, 'date':d, 'place':place, 'sensor':sensorid, 'server':hostname}
        return json

    @cherrypy.expose
    @cherrypy.tools.json_out()
    def database(self, sample='288'):
        place = sensor.placename()
        json = '''{'database': '''
        for t in read_value_from_db(int(sample)):
            json +=  '''['url': 'none', 'temp': %s, 'date' : %s, 'place': %s ], ''' % (t.temp, t.timestamp, place)
        json += ' }'
        return json

    @cherrypy.expose
    def all(self):
        urls = []
        urls.append("zerver3w.ypketron.tk")
        urls.append("192.168.1.142")
        urls.append("server.ypketron.tk")
        urls.append("zerver1.ypketron.tk")
        urls.append("zerver2.ypketron.tk")
        urls.append("roadcast.ypketron.tk")
        urls.append("192.168.1.141")
        urls.append("192.168.1.221")
        urls.append("chip1.ypketron.tk")
        urls.append("chip2.ypketron.tk")
        urls.append("frepbx.ypketron.tk")

        data = []
        for server in urls:
            url = 'http://'+server+':8805/j'
            #if ping_server(server) == False : continue
            d = getjtemp(url)
            d['url'] = server
            data.append(d)

        timestamp = datetime.strftime(datetime.now(), '%Y-%m-%d %H:%M:%S')
        tmpl = env.get_template('all.html')
        return tmpl.render(footer=footer, data=data, datetime=timestamp)

    @cherrypy.expose
    def reinit(self):
        sensor.reinit()
        place = sensor.placename()
        temp = sensor.read_temp()
        timestamp = datetime.strftime(datetime.now(), '%Y-%m-%d %H:%M:%S')

        tmpl = env.get_template('reinit.html')
        return tmpl.render(footer=footer, place=place, temp=temp, timestamp=timestamp, total_count=sensor.total_count)

    @cherrypy.expose
    def setplacename(self) :
        place = sensor.placename()
        tmpl = env.get_template('setplace.html')
        return tmpl.render(footer=footer, place=place)

    @cherrypy.expose
    def setname(self, name) :
        sensor.setplacename(name)
        return self.index()

    @cherrypy.expose
    def debug(self) :
        place = sensor.placename()
        html = sensor.sensordebug()
        html += getcputemp()
        tmpl = env.get_template('debug.html')
        return tmpl.render(footer=footer, place=place, html=html)

def getcputemp():
    import subprocess
    h = '<br>CPU '
    proc = subprocess.Popen('/opt/vc/bin/vcgencmd measure_temp', shell=True, stdout=subprocess.PIPE)
    for line in proc.stdout.readlines():
       h += line
    h += ' </br>'
    return h

def getjtemp(url):
    import requests
    try:
        r = requests.get(url, timeout=5)
        data = r.json()
    except:
        data =  {'temp':'null', 'date':'0000-00-00 00:00:00', 'place':'Unknown', 'sensor':'nil', 'server':url}
    return data

def ping_server(server):
    cmd = "ping -W 1 -c 1 %s > /dev/null 2>&1" % server
    return os.system(cmd) == 0

def writemypid(pidfile):
    pid = str(os.getpid())
    with file(pidfile, 'w') as f:
        f.write(pid)
    f.close

# Cherrypy Management
def error_page_404(status, message, traceback, version):
    tmpl = env.get_template('error.html')
    return tmpl.render(footer=footer, status=status, traceback=traceback)

# Secure headers!
def secureheaders():
    headers = cherrypy.response.headers
    headers['X-Frame-Options'] = 'DENY'
    headers['X-XSS-Protection'] = '1; mode=block'
    headers['Content-Security-Policy'] = "default-src='self'"

if __name__ == '__main__':
    import argparse
    parser = argparse.ArgumentParser()
    parser.add_argument('--port', action="store", type=int, default=8805)
    parser.add_argument('--devel', action="store_true", default=False)
    parser.add_argument('--root', action="store", default=".")
    parser.add_argument('--pid', action="store", default="/tmp/8805.pid")
    parser.add_argument('--sensehat', action="store_true", default=False)

    args = parser.parse_args()

    # Where to start, what to get
    root = os.path.abspath(args.root)
    os.chdir(root)
    current_dir = os.path.dirname(os.path.abspath(__file__))

    writemypid(args.pid)

    settings = {'global': {'server.socket_host': "0.0.0.0",
                           'server.socket_port' : args.port,
                           'log.screen': True,
                          },
               }

    conf = {'/static': {'tools.staticdir.on': True,
                        'tools.staticdir.root': current_dir,
                        'tools.staticfile.filename': 'icon.png',
                        'tools.staticdir.dir': 'static'
                    },
            '/':    {
                     'tools.auth_basic.on': False,
                     'tools.auth_basic.realm': 'localhost',
                     'tools.auth_basic.checkpassword': validate_password,
                     'tools.secureheaders.on' : True,
                     'tools.sessions.on': True,
                    },
           }


    # This is the sensor
    if args.sensehat :
        from SensorHat import Sensor
    else:
        from SensorDS18b20 import Sensor

    sensor = Sensor()

    #cherrypy.config.update(file = 'configuration.conf')
    cherrypy.config.update(settings)
    cherrypy.config.update({'error_page.404': error_page_404})
    cherrypy.tools.secureheaders = cherrypy.Tool('before_finalize', secureheaders, priority=60)

    # To make it ZERO CPU usage
    if args.devel == False:
        cherrypy.engine.timeout_monitor.unsubscribe()
        cherrypy.engine.autoreload.unsubscribe()

    # Jinja2 templates
    env = Environment(loader=FileSystemLoader('view'))

    hostname = gethostname()
    footer = {'version': version, 'hostname': hostname, 'sensor': sensor.sensorid }

    # Cherry insert pages
    serverroot = Root()

    # Start the CherryPy server.
    cherrypy.quickstart(serverroot, config=conf)

