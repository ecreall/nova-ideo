#!/bin/bash
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
DEFAULT_LOCALE="${DEFAULT_LOCALE:-en}"
ENCRYPT_DATABASE="${ENCRYPT_DATABASE:-false}"
KMI_SERVER="${KMI_SERVER:-https://encryptme.example.com}"
YAMMER_CLIENT_ID="${YAMMER_CLIENT_ID:-}"
YAMMER_CLIENT_SECRET="${YAMMER_CLIENT_SECRET:-}"
SMS_OVH_APPLICATION_KEY="${SMS_OVH_APPLICATION_KEY:-}"
SMS_OVH_APPLICATION_SECRET="${SMS_OVH_APPLICATION_SECRET:-}"
SMS_OVH_CONSUMER_KEY="${SMS_OVH_CONSUMER_KEY:-}"
SMS_OVH_ENDPOINT="${SMS_OVH_ENDPOINT:-}"
export TMPDIR="/app/var/tmp"
sed -i \
    -e "s|MAIL_HOST|$MAIL_HOST|" \
    -e "s|MAIL_PORT|$MAIL_PORT|" \
    -e "s|MAIL_USERNAME|$MAIL_USERNAME|" \
    -e "s|MAIL_PASSWORD|$MAIL_PASSWORD|" \
    -e "s|MAIL_TLS|$MAIL_TLS|" \
    -e "s|MAIL_SSL|$MAIL_SSL|" \
    -e "s|MAIL_DEFAULT_SENDER|$MAIL_DEFAULT_SENDER|" \
    -e "s|YAMMER_CLIENT_ID|$YAMMER_CLIENT_ID|" \
    -e "s|YAMMER_CLIENT_SECRET|$YAMMER_CLIENT_SECRET|" \
    -e "s|SMS_OVH_APPLICATION_KEY|$SMS_OVH_APPLICATION_KEY|" \
    -e "s|SMS_OVH_APPLICATION_SECRET|$SMS_OVH_APPLICATION_SECRET|" \
    -e "s|SMS_OVH_CONSUMER_KEY|$SMS_OVH_CONSUMER_KEY|" \
    -e "s|SMS_OVH_ENDPOINT|$SMS_OVH_ENDPOINT|" \
    -e "s|SECRET|$SECRET|" \
    -e "s|APPLICATION_URL|$APPLICATION_URL|" \
    -e "s|WORKERS|$WORKERS|" \
    -e "s|DEFAULT_LOCALE|$DEFAULT_LOCALE|" \
    production-heroku.ini
sed \
    -e "s|ENCRYPT_DATABASE|$ENCRYPT_DATABASE|" \
    -e "s|KMI_SERVER|$KMI_SERVER|" \
    etc/encryption.conf.tmpl > etc/encryption.conf
if [ -z "$MAIL_USERNAME" ]; then
    sed -i -e "s|mail.username =.*||" production-heroku.ini
fi
if [ -z "$MAIL_PASSWORD" ]; then
    sed -i -e "s|mail.password =.*||" production-heroku.ini
fi
mkdir -p var/log var/filestorage var/blobstorage var/tmp_uploads var/tmp
# create a CACHEDIR.TAG file in cache directories to not backup them
# see http://www.brynosaurus.com/cachedir/spec.html
test -f var/tmp/CACHEDIR.TAG || echo "Signature: 8a477f597d28d172789f06886806bc55" > var/tmp/CACHEDIR.TAG
test -f var/tmp_uploads/CACHEDIR.TAG || echo "Signature: 8a477f597d28d172789f06886806bc55" > var/tmp_uploads/CACHEDIR.TAG
chmod 700 var/log var/filestorage var/blobstorage var/tmp_uploads var/tmp
chmod 600 var/tmp/CACHEDIR.TAG var/tmp_uploads/CACHEDIR.TAG
chown u1000 var var/log var/filestorage var/blobstorage var/tmp_uploads var/tmp var/tmp/CACHEDIR.TAG var/tmp_uploads/CACHEDIR.TAG
sed -e 's@dace$@dace.wosystem@' -e 's@^substanced.catalogs.autosync = .*@substanced.catalogs.autosync = false@' production-heroku.ini > production-script.ini

# If this is not debian jessie (which includes varnish 4.0), assuming a more
# recent debian or ubuntu with varnish >= 4.1, replace deprecated fetch by miss in vcl_hit
grep -q jessie /etc/apt/sources.list || sed -i -e 's@.*replace by miss if varnish.*@    return (miss);@' /app/etc/varnish.vcl
mkdir /dev/varnish
# /var/lib/varnish is a symlink to /dev/varnish (tmpfs)
/usr/sbin/varnishd -P /app/var/varnishd.pid -a 0.0.0.0:5000 -f /app/etc/varnish.vcl -s malloc,256m -t 0

exec ./start_all.bash production-heroku.ini $TIMEOUT
