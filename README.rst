=========
Nova Ideo
=========

Features
--------

See `nova-ideo.com <https://www.nova-ideo.com/>`__


Translations
------------

This product has been translated into

- English
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

The app is deployed on https://local.ecreall.com:8443
(local.ecreall.com resolves to 127.0.0.1 and is necessary for nginx)

To send emails, you need to configure the MAILER variables in
**docker-compose-dev.yml**
The default configuration is used to connect with a postfix via a ssh tunnel
like this::

    ssh -L 172.17.0.1:9025:localhost:25 myserver.example.com


Deployment with docker
----------------------

Clone a specific version::

    git clone -b VERSION git@github.com:ecreall/nova-ideo.git
    cd nova-ideo

(replace VERSION with the latest release, 1.1 for example)

docker-compose runs a nginx container on port 80 and 443.
You need to edit the **nginx-app-prod.conf** file to replace mynovaideo.example.com
by your domain and add certificates (**server.key** and **server.crt**) to the
**tls** directory.

You need to configure some environment variables, copy the file
**docker-compose.override.yml.templ** to **docker-compose.override.yml** and edit it.

- SECRET: the initial admin password
- APPLICATION_URL: your domain, same as you put in nginx-app-prod.conf
- MAIL_DEFAULT_SENDER: the sender of the mails that the application use
- MAILER_HOST: SMTP host
- MAILER_PORT: SMTP port
- MAILER_USERNAME: SMTP username
- MAILER_PASSWORD: SMTP password
- MAILER_TLS: Use TLS
- MAILER_SSL: Use SSL

If you want to connect to a postfix container, there is a commented example
in **docker-compose.override.yml.templ** that use an external postfix container
connected on a mybridge bridge network. You need to create a mybridge bridge
network and start a postfix container yourself. (not documented here)

To deploy::

    sudo docker-compose up -d

To connect with the super administrator (for the evolve steps and to create
an other admin account only), go to
https://mynovaideo.example.com/manage
and log in with "admin" and the password is the one you gave in the SECRET
environment variable.

After the initial connection, you can increase the number of workers that are
used to handle the requests in **docker-compose.override.yml** and run again
**sudo docker-compose up -d** (WORKERS=3 is a good default).


How to upgrade your install
---------------------------

For each release, a docker image is built and the **docker-compose.yml** is
modified accordingly.

If you previously cloned the repository with version 1.0, to upgrade to 1.1 for
example, do::

    git checkout 1.1
    sudo docker-compose up -d

After that, be sure to execute the evolve steps by connecting with the super
administrator at https://mynovaideo.example.com/manage
and going to *Database* tab, and click on *Evolve* red button. You can see
the evolve steps with the *Summarize* button.


Backup and maintainance of your database
----------------------------------------

Your data is in the var folder, be sure to backup it.

The database is a ZODB filestorage, you should pack it regularly (every week)
to reduce its size. Example of cron for user root run at 1am sunday:

    0 1 * * 0 docker exec novaideo_novaideo_1 /app/bin/zeopack -d 1 -u /app/var/zeo.sock

Be sure that the container name is novaideo_novaideo_1 in your case. You can
verify it with **docker ps**.

