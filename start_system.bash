#!/bin/bash
sleep 60s
sed -e 's@dace.wosystem@dace.wosystem dace.system@' \
    -e 's@^substanced.catalogs.autosync = .*@substanced.catalogs.autosync = false@' \
    -e 's@^port = .*@port = 5002@' \
    -e 's@^host = .*@host = 127.0.0.1@' \
    -e 's@^workers =.*@workers = 1@' $1 > production-system.ini
exec ./bin/gunicorn --access-logfile - --paste production-system.ini -t 36000
