#!/bin/bash
inifile=$1
TIMEOUT=$2
nginxcontainer=$(awk '/novaideo_nginx_1/{print $1}' /etc/hosts)
# 127.0.0.1 is when varnish->gunicorn in the same container
# 172.17.42.1 is for dokku : nginx host->gunicorn container
# $nginxcontainer is for nginx container->gunicorn container
exec gosu u1000 ./codep \
    './bin/runzeo -C etc/zeo.conf' \
    "./bin/gunicorn --forwarded-allow-ips=127.0.0.1,172.17.42.1,$nginxcontainer --access-logfile - --paste $inifile -t $TIMEOUT" \
    "./start_system.bash $inifile"
