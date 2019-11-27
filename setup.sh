#!/bin/bash

#To set up the python enviroment:
python3 -m venv env
source env/bin/activate
pip install -r requirements.txt
deactivate
