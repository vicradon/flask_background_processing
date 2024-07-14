#!/bin/bash
source .venv/bin/activate
exec gunicorn -w 2 -k eventlet -b 0.0.0.0:5000 app:app
