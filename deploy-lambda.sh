#!/bin/bash

cd serverless
sls deploy --region eu-central-1 --aws-profile serverless-admin
cd ..