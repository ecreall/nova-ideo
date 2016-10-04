#!/bin/bash
sed -i 's@/tmp/build@/app@' develop-eggs/* bin/*
# MAIL_HOST may be defined if you did a postfix:mail link and it will be
# something like tcp://172.17.0.3:25, we don't want that.
# We want the default 'mail', so we use MAILER_HOST environment variable.
MAIL_HOST="${MAILER_HOST:-mail}"
MAIL_PORT="${MAILER_PORT:-25}"
MAIL_USERNAME="${MAILER_USERNAME:-}"
MAIL_PASSWORD="${MAILER_PASSWORD:-}"
MAIL_TLS="${MAILER_TLS:-false}"
MAIL_SSL="${MAILER_SSL:-false}"
MAIL_DEFAULT_SENDER="${MAIL_DEFAULT_SENDER:-noreply@example.com}"
SECRET="${SECRET:-mybigsecret}"
APPLICATION_URL="${APPLICATION_URL:-https://mynovaideo.example.com}"
TIMEOUT="${TIMEOUT:-300}"
WORKERS="${WORKERS:-1}"
export TMPDIR="/app/var/tmp"
sed -i \
    -e "s|MAIL_HOST|$MAIL_HOST|" \
    -e "s|MAIL_PORT|$MAIL_PORT|" \
    -e "s|MAIL_USERNAME|$MAIL_USERNAME|" \
    -e "s|MAIL_PASSWORD|$MAIL_PASSWORD|" \
    -e "s|MAIL_TLS|$MAIL_TLS|" \
    -e "s|MAIL_SSL|$MAIL_SSL|" \
    -e "s|MAIL_DEFAULT_SENDER|$MAIL_DEFAULT_SENDER|" \
    -e "s|SECRET|$SECRET|" \
    -e "s|APPLICATION_URL|$APPLICATION_URL|" \
    -e "s|WORKERS|$WORKERS|" \
    production-heroku.ini
if [ -z "$MAIL_USERNAME" ]; then
    sed -i -e "s|mail.username =.*||" production-heroku.ini
fi
if [ -z "$MAIL_PASSWORD" ]; then
    sed -i -e "s|mail.password =.*||" production-heroku.ini
fi
mkdir -p var/log var/filestorage var/blobstorage var/tmp_uploads var/tmp
chmod 700 var/log var/filestorage var/blobstorage var/tmp_uploads var/tmp
chown u1000 var var/log var/filestorage var/blobstorage var/tmp_uploads var/tmp
sed -e 's@dace$@dace.wosystem@' -e 's@^substanced.catalogs.autosync = .*@substanced.catalogs.autosync = false@' production-heroku.ini > production-script.ini
/usr/sbin/varnishd -P /app/var/varnishd.pid -a 0.0.0.0:5000 -f /app/etc/varnish.vcl -s malloc,256m -t 0
exec ./start_all.bash production-heroku.ini $TIMEOUT
