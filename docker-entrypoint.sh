#!/bin/bash

echo "Applying database migrations..."
python manage.py migrate

echo "Collecting static files..."
python manage.py collectstatic --noinput

echo "Starting Celery worker..."
celery -A backend.celery_app worker -l info &

# Delay Celery Beat until migrations are applied
echo "Starting Celery Beat..."
celery -A backend.celery_app beat -l info --scheduler django_celery_beat.schedulers:DatabaseScheduler
