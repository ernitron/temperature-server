#
# My Web Temp Server
# ernitron (c) 2013
#


# Variables
SERVER=server
SERVERS=server server1 server2 chip1 chip2
SCRIPT=tempserver.sh
INSTALLDIR=/usr/local/bin/tempserver
STATIC = static
VIEW = view
PACKAGES= server.py \
          SensorDS18b20.py \
          SensorHat.py \
		  DatabaseModel.py \
		  TemperatureDemon.py \

run: check
	python server.py --devel --port 8805 &

check:
	python -m py_compile *.py
	rm -f *.pyc

clean:
	rm -f *.pyc

requirements: check
	echo python-cherrypy3 > requirements.txt
	echo sqlite3 >> requirements.txt
	echo requests >> requirements.txt
	echo install `cat requitements.txt`

start:
	sudo /etc/init.d/$(SCRIPT) start

stop:
	sudo /etc/init.d/$(SCRIPT) stop


