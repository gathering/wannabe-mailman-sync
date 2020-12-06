#!/bin/sh

cd /opt
python -m pip install -r requirements.txt
python -m pip install git+https://gitlab.com/mailman/mailmanclient
python main.py
sleep 1800
