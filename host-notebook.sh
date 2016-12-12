#!/usr/bin/env bash
docker-compose -f docker-compose-science.yml build
docker-compose run -p 8888:8888 -e NOTEBOOK_PASS_HASH web /bin/bash /usr/src/app/turkey/run-notebook-server.sh;
