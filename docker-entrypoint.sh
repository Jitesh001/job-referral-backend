#!/bin/bash

# Apply database migrations
echo "Applying database migrations"
python manage.py migrate

# Collect static files
echo "Running collect static"
python manage.py collectstatic --noinput

# Start server
echo "Starting server"
gunicorn backend.wsgi:application --bind 0.0.0.0:8000 & celery -A backend.celery_app worker -l info & celery -A backend.celery_app beat -l info --scheduler django_celery_beat.schedulers:DatabaseScheduler
