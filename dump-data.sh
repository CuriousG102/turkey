#!/usr/bin/env bash
docker-compose -f docker-compose-science.yml build;
(docker-compose run -e SECRET_KEY=whocares web python /usr/src/app/turkey/manage.py dumpdata) > databasefile;