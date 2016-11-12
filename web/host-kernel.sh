#!/usr/bin/env bash
DEBUG=1;
export DEBUG;
openssl req -x509 -nodes -days 365 -newkey rsa:1024 -keyout mykey.key -out mycert.pem;
python /usr/src/app/turkey/manage.py shell_plus --notebook --no-browser;
