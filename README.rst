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

::

    sudo docker-compose up -d


Currently, you need an external container named postfix on a mybridge bridge
network with exposed port 25 to send emails.
docker-compose runs a nginx container on port 80 and 443.
You need to create the nginx-app-prod.conf file (similar to nginx-app-dev.conf)
and add certificates to the local tls directory.

