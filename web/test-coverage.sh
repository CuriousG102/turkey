#!/usr/bin/env bash
bash ./wait-for-it.sh -t 30 -h postgres -p 5432;
bash setup.sh;
coverage run --source='turkey' turkey/manage.py test survey.tests;
coverage report;
