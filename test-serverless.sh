#!/bin/bash

sls invoke local -f hello -p data/request_data/invoke-get-imageurl.json -l
sls invoke local -f hello -p data/request_data/invoke-post-base64-image.json -l