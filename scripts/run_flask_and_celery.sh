#!/bin/bash

source .venv/bin/activate
exec gunicorn -b 0.0.0.0:5000 app:app
exec celery -A background_tasks.tasks worker --loglevel=info