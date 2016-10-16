#!/usr/bin/env bash
bash ./wait-for-it.sh -t 30 -h postgres -p 5432;
bash ./wait-for-it.sh -t 30 -h selenium -p 4444;
bash setup.sh;
python /usr/src/app/turkey/manage.py test --liveserver=0.0.0.0:8082-8090 survey.tests;
