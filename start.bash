#!/bin/bash
sed -i 's@/tmp/build@/app@' develop-eggs/* bin/*
exec bin/gunicorn --paste production.ini
