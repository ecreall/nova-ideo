#!/bin/bash
inifile=$1
TIMEOUT=$2
# 127.0.0.1 is when varnish->gunicorn in the same container
exec gosu u1000 ./codep \
    "./bin/gunicorn --forwarded-allow-ips=127.0.0.1 --access-logfile - --paste $inifile -t $TIMEOUT" \
    './bin/runzeo -C etc/zeo.conf' \
    "./start_system.bash $inifile"
