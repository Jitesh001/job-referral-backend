#!/bin/bash

set -e  # Exit if any command fails

echo "Running database migrations..."
python manage.py migrate

echo "Starting Celery worker..."
celery -A backend.celery_app worker -l info &
CELERY_WORKER_PID=$!

echo "Starting Celery Beat..."
celery -A backend.celery_app beat -l info --scheduler django_celery_beat.schedulers:DatabaseScheduler &
CELERY_BEAT_PID=$!

echo "Starting Gunicorn..."
exec gunicorn backend.wsgi:application --bind 0.0.0.0:8000
