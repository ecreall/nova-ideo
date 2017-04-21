#!/bin/bash
inifile=$1
TIMEOUT=$2
# 127.0.0.1 is when varnish->gunicorn in the same container
# /dev is a tmpfs in a docker container, use that for worker-tmp-dir, see
# http://docs.gunicorn.org/en/stable/faq.html#how-do-i-avoid-gunicorn-excessively-blocking-in-os-fchmod
mkdir /dev/tmp
chown u1000:u1000 /dev/tmp
exec gosu u1000 ./codep \
    "./bin/gunicorn --forwarded-allow-ips=127.0.0.1 --access-logfile - --paste $inifile -t $TIMEOUT --worker-tmp-dir /dev/tmp" \
    './bin/runzeo -C etc/zeo.conf' \
    "./start_system.bash $inifile"
