#
# My Web Radio Server
# ernitron (c) 2013
#
#
## Color definition. Stolen from gentoo ;)
# normally no changes needed to this settings
GOOD=$'\e[32;01m'
WARN=$'\e[33;01m'
BAD=$'\e[31;01m'
NORMAL=$'\e[0m'
HILITE=$'\e[36;01m'
BRACKET=$'\e[34;01m'
#


# Variables
SERVER=roadcast-e
SERVERS=server zerver1 zerver2 zerver3w chip1 chip2 frepbx roadcast-e wifi1
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
	python server.py --devel --port 8888 &

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

ssh: check		
	for s in server zerver1 zerver2 zerver3 chip1 chip2; \
	do \
	   echo Doing something in $$s ;\
	   #scp $(SERV) root@$$s:/$(INSTALLDIR) ;\
	   ssh  root@$$s /etc/init.d/tempserver.sh restart ;\
	   #ssh  root@$$s mv $(INSTALLDIR)/all.html $(INSTALLDIR)/view ;\
	done;

rsync: check		
	for s in $(SERVERS); \
	do \
	   #echo scp $(PACKAGES) root@$$s:/$(INSTALLDIR) ;\
	   #scp $(PACKAGES) root@$$s:/$(INSTALLDIR) ;\
	   #scp server.py root@$$s:/$(INSTALLDIR) ;\
	   #ssh  root@$$s  $(INSTALLDIR)/tempserver.sh stop ;\
	   rsync -av $(PACKAGES) $(VIEW) $(STATIC) $(SCRIPT) root@$$s:/$(INSTALLDIR)/ ;\
	   #ssh  root@$$s  $(INSTALLDIR)/tempserver.sh start ;\
	done;

rsync1: check
	#rsync -av --exclude '*.db' --exclude '.git' --exclude 'Makefile' --exclude 'STUFF' --exclude 'BACKUP' --exclude '*.pid' --exclude '*.pyc' ./ root@$(SERVER):/$(INSTALLDIR)/
	rsync -av *.py ./static root@$(SERVER):/$(INSTALLDIR)/

syncfromtarget:
	rsync -av -n --exclude '.git' --exclude '*.pid' --exclude '*.pyc'  root@$(SERVER):/$(INSTALLDIR)/ .

start:
	sudo /etc/init.d/$(SCRIPT) start

stop:
	sudo /etc/init.d/$(SCRIPT) stop


