#!/usr/bin/env bash
bash ./wait-for-it.sh -t 60 -h postgres -p 5432;
bash ./wait-for-it.sh -t 60 -h selenium-chrome -p 4444;
bash setup.sh;
if [ $# -eq 0 ]
then
    python /usr/src/app/turkey/manage.py test --parallel --liveserver=0.0.0.0:8082-8097 survey.tests;
else
    python /usr/src/app/turkey/manage.py test --liveserver=0.0.0.0:8082-8097 survey.tests.$1;
fi
