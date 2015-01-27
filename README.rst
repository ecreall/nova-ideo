Getting Started
===============

On your machine (for development/demo)
--------------------------------------

Without Docker::

  python3.4 bootstrap.py
  bin/buildout
  bin/pserve production.ini

The application is on http://localhost:5000

You may need to configure the mail host and port on production.ini.

With Docker and Docker Compose (for local tests only)::

  mkvirtualenv compose
  pip install --pre docker-compose
  make
  docker-compose up

The app is deployed on http://local.ecreall.com:8080


With Dokku (for production)
---------------------------

Requirements:

- a Dokku install on a server
- a postfix container running on your server
- a wildcard certificate in /home/dokku/tls/
- you can push apps to your server

::

  APP=novaideo
  git clone git@github.com:ecreall/nova-ideo.git $APP
  cd $APP
  ssh dokku@dokku.me apps:create $APP
  ssh dokku@dokku.me config:set $APP BUILDOUT_CFG=heroku.cfg
  ssh dokku@dokku.me config:set $APP SECRET=mybigsecret
  ssh dokku@dokku.me config:set $APP APPLICATION_URL=https://$APP.dokku.me
  ssh dokku@dokku.me config:set $APP MAIL_DEFAULT_SENDER=contact@example.com
  ssh dokku@dokku.me link:create $APP postfix mail
  ssh dokku@dokku.me docker-options:add $APP "-v /home/dokku/$APP/.volumes/var:/app/var"
  git remote add deploy dokku@dokku.me:$APP
  git push deploy master
