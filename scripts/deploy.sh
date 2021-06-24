#! /usr/bin/env sh

# Exit in case of error
set -e

STACK_NAME=${STACK_NAME} \
TAG=${TAG} \
docker-compose \
-f docker-compose.yml \
config > docker-stack.yml

docker-auto-labels docker-stack.yml

docker stack deploy --with-registry-auth --resolve-image changed -c docker-stack.yml --with-registry-auth "${STACK_NAME}"
