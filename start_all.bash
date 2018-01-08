#!/bin/bash
inifile=$1
TIMEOUT=$2
WORKERS=$3
# 127.0.0.1 is when varnish->gunicorn in the same container
# /dev is a tmpfs in a docker container, use that for worker-tmp-dir, see
# http://docs.gunicorn.org/en/stable/faq.html#how-do-i-avoid-gunicorn-excessively-blocking-in-os-fchmod
mkdir /dev/tmp
chown u1000:u1000 /dev/tmp
if [[ $WORKERS == 0 ]]; then
  exec gosu u1000 ./codep './bin/runzeo -C etc/zeo.conf'
elif [[ $WORKERS == 1 ]]; then
  sed -i -e 's@dace.wosystem@dace@' $inifile
  exec gosu u1000 ./codep \
    "./bin/gunicorn --forwarded-allow-ips=127.0.0.1 --access-logfile - --paste $inifile -t $TIMEOUT --worker-tmp-dir /dev/tmp" \
    './bin/runzeo -C etc/zeo.conf'
else
  exec gosu u1000 ./codep \
    "./bin/gunicorn --forwarded-allow-ips=127.0.0.1 --access-logfile - --paste $inifile -t $TIMEOUT --worker-tmp-dir /dev/tmp" \
    './bin/runzeo -C etc/zeo.conf' \
    "./start_system.bash $inifile"
fi
