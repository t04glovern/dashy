#!/bin/bash

## Stop Systemctl service
sudo systemctl stop dashy

## Git Pull
git pull

## Install pip requirements
WORKING_DIR=/home/nathan/Production/dashy
ACTIVATE_PATH=/home/nathan/.virtualenvs/flask-python2.7-dev/bin/activate
cd ${WORKING_DIR}
source ${ACTIVATE_PATH}
pip install -r requirements.txt

## Restart Systemctl service
sudo systemctl start dashy
