#!/bin/bash

#Google api key
export GOOGLE_APPLICATION_CREDENTIALS="$(pwd)/api_key.json"

#Run the server
source env/bin/activate
cd speakeasy
flask run
deactivate
