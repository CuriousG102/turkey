#!/usr/bin/env bash
DEBUG=1;
export DEBUG;
python /usr/src/app/turkey/manage.py shell_plus --notebook --no-browser;
