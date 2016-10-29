#!/usr/bin/env bash
docker-compose -f docker-test-compose.yml build;
docker network create test_net;
docker run --network="test_net" --network-alias="postgres" turkey_postgres &
docker run --network="test_net" --network-alias="selenium-chrome" selenium/standalone-chrome &
if [ $# -eq 0 ]
then
    docker run --network="test_net" --network-alias="web" --env-file .test-env turkey_web ./test.sh;
else
    docker run --network="test_net" --network-alias="web" --env-file .test-env turkey_web ./test.sh $1;
fi
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
