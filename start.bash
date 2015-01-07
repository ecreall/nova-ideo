#!/bin/bash
sed -i 's@/tmp/build@/app@' develop-eggs/* bin/*
exec bin/gunicorn --forwarded-allow-ips="172.17.42.1" --paste production.ini
