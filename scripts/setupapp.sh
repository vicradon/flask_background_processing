#!/bin/bash

python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt

sudo mkdir -p /var/log
sudo touch /var/log/messaging_system.log