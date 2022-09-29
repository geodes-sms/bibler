#!/bin/bash
a2enconf mod-wsgi
/usr/sbin/apache2ctl -D FOREGROUND
service apache2 restart
