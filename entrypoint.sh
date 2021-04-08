#!/bin/sh

apk update && apk upgrade
apk add --no-cache git
cd /opt
python -m pip install -r requirements.txt
python -m pip install git+https://gitlab.com/mailman/mailmanclient
python main.py
