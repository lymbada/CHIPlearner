#!/bin/sh
if [ -f /var/run/dbus.pid ]
then
	echo "the /var/run/dbus.pid file exists, removing before starting dbus"
	rm /var/run/dbus.pid
fi

/usr/bin/dbus-daemon --system &&
echo "dbus service started with code:$?"

exit_script(){
	/usr/sbin/avahi-daemon --kill
	echo "avahi-deamon killed with code $?"

	if [ -f /var/run/dbus.pid ]
	then
		echo "the /var/run/dbus.pid file exists, removing because shutting down"
		rm /var/run/dbus.pid
			echo "just killed dbus.pid file with $? code"
	fi

	exit 0
}

trap exit_script 0 2 3 15 SIGINT SIGTERM
/usr/sbin/avahi-daemon --daemonize
echo "avahi-daemon started with code:$?"

while [ True ]
do
	sleep 2
done
