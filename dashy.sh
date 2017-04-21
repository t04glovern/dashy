#!/bin/bash

## Stop Systemctl service
sudo systemctl stop dashy

## Git Pull
git pull

## Restart Systemctl service
sudo systemctl start dashy
