=========
Nova Ideo
=========

Features
--------

See `nova-ideo.com <https://nova-ideo.com/>`__


Translations
------------

This product has been translated into

- French


Contribute
----------

- Issue Tracker: https://github.com/ecreall/nova-ideo/issues
- Source Code: https://github.com/ecreall/nova-ideo


License
-------

The project is licensed under the GPLv3.


Getting Started for development
-------------------------------

To run in development mode (without docker)::

    python3.4 bootstrap.py
    bin/buildout
    bin/runzeo -C etc/zeo.conf
    bin/pserve development.ini

The application is on http://localhost:6543

To execute all processes with docker (almost same as production)::

    sudo docker-compose -f docker-compose-dev.yml pull
    sudo docker-compose -f docker-compose-dev.yml build --pull
    sudo docker-compose -f docker-compose-dev.yml rm -f
    sudo docker-compose -f docker-compose-dev.yml up -d

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
