#!/bin/bash
source .venv/bin/activate
exec celery -A background_tasks.tasks worker --loglevel=info
