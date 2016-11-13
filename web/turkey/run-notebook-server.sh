#!/usr/bin/env bash
cd turkey;
DEBUG=1;
export DEBUG;
DJANGO_SETTINGS_MODULE=turkey.settings;
export DJANGO_SETTINGS;
openssl req -x509 -nodes -days 365 -newkey rsa:1024 -keyout mykey.key -out mycert.pem;
jupyter notebook --config=/usr/src/app/turkey/jupyter_config.py
