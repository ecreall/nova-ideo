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

The project is licensed under the AGPLv3+.


Getting Started for development
-------------------------------

To run in development mode without docker::

    python3.4 bootstrap.py
    bin/buildout
    bin/runzeo -C etc/zeo.conf
    bin/pserve development.ini

The application is on http://localhost:6543


To run in development mode with docker::

    ./run.sh rebuild
    ./run.sh

The app is deployed on http://local.ecreall.com:8080

To send emails, you need a mta agent on 172.17.0.1:9025.
If you have a server with postfix, you can do a tunnel like so::

    ssh -L 172.17.0.1:9025:localhost:25 myserver.example.com


Deployment with docker
----------------------

Currently, you need an external container named postfix on a mybridge bridge
network with exposed port 25 on the network to send emails.

docker-compose runs a nginx container on port 80 and 443.
You need to edit the nginx-app-prod.conf file to replace mynovaideo.example.com
by your domain and add certificates (server.key and server.crt) to the
tls directory.

You need to configure some environment variables, copy the file
docker-compose.override.yml.templ to docker-compose.override.yml and edit it.

- SECRET: the initial admin password
- APPLICATION_URL: your domain, same as you put in nginx-app-prod.conf
- MAIL_DEFAULT_SENDER: the sender of the mails that the application use

To deploy::

    sudo docker-compose up -d

To connect with the super administrator (for the evolve steps and to create
an other admin account only), go to
https://mynovaideo.example.com/manage
and log in with "admin" and the password is the one you gave in the SECRET
environment variable.

You can go to Services and then Databases to see if there is any evolve steps
to do.


Your data is in the var folder, be sure to backup it.

The database is a ZODB filestorage, you should pack it regularly (every week)
to reduce its size. Example of cron run at 1am sunday:

    0 1 * * 0 docker exec novaideo_novaideo_1 /app/bin/zeopack -d 1 -u /app/var/zeo.sock

Be sure that the container name is novaideo_novaideo_1 in you case.

