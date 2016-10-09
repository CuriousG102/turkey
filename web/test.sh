#!/usr/bin/env bash
bash ./wait-for-it.sh -t 30 -h postgres -p 5432;
bash setup.sh;
python /usr/src/app/turkey/manage.py test survey.tests;
