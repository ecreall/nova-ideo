#!/bin/bash
sed -i 's@/tmp/build@/app@' develop-eggs/* bin/*
MAIL_HOST="${MAIL_PORT_25_TCP_ADDR:-localhost}"
MAIL_PORT="${MAIL_PORT_25_TCP_PORT:-25}"
MAIL_DEFAULT_SENDER="${MAIL_DEFAULT_SENDER:-site@example.com}"
SECRET="${SECRET:-dreevTatUk9}"
APPLICATION_URL="${APPLICATION_URL:-applicationurl}"
sed -i \
    -e "s|MAIL_HOST|$MAIL_HOST|" \
    -e "s|MAIL_PORT|$MAIL_PORT|" \
    -e "s|MAIL_DEFAULT_SENDER|$MAIL_DEFAULT_SENDER|" \
    -e "s|SECRET|$SECRET|" \
    -e "s|APPLICATION_URL|$APPLICATION_URL|" \
    production-heroku.ini
mkdir -p var/filestorage var/blobstorage
chmod 700 var/filestorage var/blobstorage
exec bin/gunicorn --forwarded-allow-ips="172.17.42.1" --access-logfile var/access.log --paste production-heroku.ini
