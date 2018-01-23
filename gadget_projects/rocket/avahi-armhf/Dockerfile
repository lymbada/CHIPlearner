FROM armhf/alpine

RUN apk update && apk add avahi	dbus

ADD start.sh /start.sh
ADD services /etc/avahi/services
ADD avahi-daemon.conf /etc/avahi/avahi-daemon.conf

ENTRYPOINT ["/start.sh"]