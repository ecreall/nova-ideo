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

without docker
~~~~~~~~~~~~~~

To run in development mode without docker::

    sudo apt-get install python3 python3-dev libxml2-dev libxslt1-dev \
      libjpeg-dev zlib1g-dev libfreetype6-dev libtiff5-dev libzmq3-dev \
      libyaml-dev git  # this is working on debian jessie and ubuntu xenial
    python3 bootstrap.py
    mkdir -p var/{filestorage,blobstorage,log}
    bin/buildout  # It takes a long time...
    bin/runzeo -C etc/zeo.conf  # It starts in foreground, there is no output.  Use Ctrl+C to stop it.
    bin/pserve development.ini  # in another terminal

The application is on http://localhost:6543

I'll use $DOMAIN for http://localhost:6543 in the rest of the documentation.

To send emails with gmail smtp, you need to uncomment some lines and configure
the mail and password in development.ini


with docker
~~~~~~~~~~~

You first need to install the `docker engine
<https://docs.docker.com/engine/installation/linux/>`__ and
`docker-compose <https://docs.docker.com/compose/install/>`__.

To run in development mode with docker::

    ./run.sh rebuild
    ./run.sh

The app is deployed on https://local.ecreall.com:8443
(local.ecreall.com resolves to 127.0.0.1 and is necessary for nginx)

I'll use $DOMAIN for https://local.ecreall.com:8443 in the rest of the documentation.

The default configuration in **docker-compose-dev.yml** is used to connect
with a postfix via a ssh tunnel like this::

    ssh -L 172.17.0.1:9025:localhost:25 myserver.example.com

To send emails with gmail smtp instead, you need to configure the MAILER
variables in **docker-compose.override.yml**, copy the file
**docker-compose.override.yml.templ** to **docker-compose.override.yml** and
edit it. This will overrides the configuration in **docker-compose-dev.yml**.

To stop the application, do a Ctrl-c, and to stop the other containers (nginx),
run::

    ./run.sh down


Allow your gmail account to be used to send emails
--------------------------------------------------

To allow your gmail account to be used to send emails, you need to enable
`less secure apps <https://support.google.com/accounts/answer/6010255>`__ and
do the `captcha <https://support.google.com/accounts/answer/6009563>`__.
Look at the logs in the terminal if you have an error when sending a mail.

Be careful to not commit your gmail password!
The ini file doesn't support the use of % character in your password.
It thinks it's the beginning of a variable.
If you use this character in your password, you will need to change it!

How to assign roles to a person
-------------------------------

If you want to give a person some additional roles, you need to have the
*Administrator* or *Site administrator* role. The first time, you will need to
do it with the special super administrator account.
Go to $DOMAIN/manage (there is no accessible link from the home page)
and authenticate with login admin and the password
you have in SECRET environment variable
(It's substanced.initial_password key in development.ini if you use the
install without docker).
Return to $DOMAIN and go the hamburger menu on the top left, select
See/Members, go to a person's profile, click on *Assign
roles* button and give her the *Site administrator*, *Examiner* or *Moderator*
role.


Deployment with docker
----------------------

Clone a specific version::

    git clone -b VERSION git@github.com:ecreall/nova-ideo.git
    cd nova-ideo

(replace VERSION with the latest release, 1.2 for example)

docker-compose runs a nginx container on port 80 and 443.
You need to edit the **nginx-app-prod.conf** file to replace mynovaideo.example.com
by your domain and add certificates (**server.key** and **server.crt**) to the
**tls** directory.

Be sure that in **docker-compose.yml** it uses the correct version
ecreall/novaideo:release-VERSION. Edit it if it's not the case.

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
- LOGO_FILENAME: empty by default to use the Nova-Ideo logo. You can
  set the variable to 'marianne.svg' or other images included in the
  novaideo/static/images/ directory to configure the logo when the application
  is created.

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

To see the logs::

    docker-compose logs -f


How to upgrade your install
---------------------------

For each release, a docker image is built and the **docker-compose.yml** is
modified accordingly.

If you previously cloned the repository with version 1.1, to upgrade to 1.2 for
example, do::

    git checkout 1.2
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

