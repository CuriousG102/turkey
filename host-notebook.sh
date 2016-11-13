#!/usr/bin/env bash
docker-compose run -p 8888:8888 web /bin/bash /usr/src/app/turkey/run-notebook-server.sh;
