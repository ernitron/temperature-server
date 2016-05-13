#!/bin/sh

### BEGIN INIT INFO
# Provides:        tempserver
# Required-Start:  $network $remote_fs $syslog
# Required-Stop:   $network $remote_fs $syslog
# Default-Start:   2 3 4 5
# Default-Stop:    0 1 6
# Short-Description: Start temploop daemon
### END INIT INFO

PATH=/sbin:/bin:/usr/sbin:/usr/bin:/usr/local/sbin:/usr/local/bin

. /lib/lsb/init-functions

SERVERNAME=looptemp
DIRECTORY=/usr/local/bin/tempserver
DAEMON=/usr/local/bin/tempserver/TemperatureLoop.py
PIDFILE=/var/run/temploop.pid
OPTS="--root /usr/local/bin/tempserver --pid $PIDFILE"
LOCKFILE=/var/lock/tempserver

#------ There should be NO need to change below --------------

test -x $DAEMON || exit 5

lock_server() {
	if [ -x /usr/bin/lockfile-create ]; then
		lockfile-create $LOCKFILE
		lockfile-touch $LOCKFILE &
		LOCKTOUCHPID="$!"
	fi
}

unlock_server() {
	if [ -x /usr/bin/lockfile-create ] ; then
		kill $LOCKTOUCHPID
		lockfile-remove $LOCKFILE
	fi
}

RUNASUSER=root
UGID=$(getent passwd $RUNASUSER | cut -f 3,4 -d:) || true
if test "$(uname -s)" = "Linux"; then
        OPTS="$OPTS "
fi

case $1 in
	start)
		log_daemon_msg "Starting $SERVERNAME"
		if [ -z "$UGID" ]; then
			log_failure_msg "user \"$RUNASUSER\" does not exist"
			exit 1
		fi
		lock_server
  		start-stop-daemon --chdir $DIRECTORY --start --quiet --oknodo --background --pidfile $PIDFILE --startas $DAEMON -- $OPTS
		status=$?
		unlock_server
		log_end_msg $status
  		;;
	kill)
		log_daemon_msg "Stopping $SERVERNAME"
        killall $DAEMON
		log_end_msg $?
		rm -f $PIDFILE
  		;;
	stop)
		log_daemon_msg "Stopping $SERVERNAME"
  		start-stop-daemon --stop --quiet --oknodo --pidfile $PIDFILE
		log_end_msg $?
		rm -f $PIDFILE
  		;;
	restart|force-reload)
		$0 stop && sleep 2 && $0 start
  		;;
	try-restart)
		if $0 status >/dev/null; then
			$0 restart
		else
			exit 0
		fi
		;;
	reload)
		exit 3
		;;
	status)
        status_of_proc -p $PIDFILE $DAEMON "$SERVERNAME server"
		;;
	*)
		echo "Usage: $0 {start|stop|restart|try-restart|force-reload|status}"
		exit 2
		;;
esac
