#!/bin/bash

pm2 start scripts/run_flask_and_celery.sh
pm2 save