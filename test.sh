#!/usr/bin/env bash
docker-compose -f docker-test-compose.yml build;
docker network create test_net;
docker run --network="test_net" --network-alias="postgres" turkey_postgres &
docker run --network="test_net" --network-alias="selenium" selenium/standalone-chrome &
docker run --network="test_net" --network-alias="web" --env-file .test-env turkey_web ./test.sh;
if [ $? -eq 0 ]
then
  echo "Success";
  docker stop $(docker ps -q);
  docker network rm test_net;
  exit 0;
else
  echo "Failure";
  docker stop $(docker ps -q);
  docker network rm test_net;
  exit 1;
fi
