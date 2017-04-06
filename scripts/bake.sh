#!/bin/bash
set -o allexport

DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"
cd $DIR/..

if [ -e .env ]; then
	source .env
fi
echo $FRIDAY_DEMO2_DOCKER_IMAGE_LOCAL

docker build -t $FRIDAY_DEMO2_DOCKER_IMAGE_LOCAL:$FRIDAY_DEMO2_IMAGE_VERSION . 
