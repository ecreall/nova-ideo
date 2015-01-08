#!/bin/bash
sed -i 's@/tmp/build@/app@' develop-eggs/* bin/*
SECRET="${SECRET:-dreevTatUk9}"
SENDER="${SENDER:-site@example.com}"
APPLICATION_URL="${APPLICATION_URL:-novaideo-applicationurl}"
sed -i \
    -e "s|SECRET|$SECRET|" \
    -e "s|SENDER|$SENDER|" \
    -e "s|APPLICATION_URL|$APPLICATION_URL|" \
    production-heroku.ini
exec bin/gunicorn --forwarded-allow-ips="172.17.42.1" --paste production-heroku.ini
