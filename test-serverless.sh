#!/bin/bash

DOCKER_CONTAINER_ID=$(docker run -d -v "$PWD":/dynamodb_local_db -p 8000:8000 cnadiminti/dynamodb-local:latest)
python dynamodb-local-cloud-formation/parse.py --region eu-central-1 --endpoint-url http://localhost:8000 dynamodb.yml | sh
sls invoke local -f hello -p data/request_data/invoke-get-imageurl.json -l
sls invoke local -f hello -p data/request_data/invoke-post-base64-image.json -l
docker stop $DOCKER_CONTAINER_ID
echo "TEST FINISHED"