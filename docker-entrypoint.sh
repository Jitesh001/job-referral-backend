#!/bin/bash

# Exit on any error
set -e

echo "Waiting for PostgreSQL to be ready..."
until pg_isready -h "$DB_HOST" -p "$DB_PORT" -U "$POSTGRES_USER"; do
  sleep 1
done

echo "Applying database migrations..."
python manage.py migrate

echo "Collecting static files..."
python manage.py collectstatic --noinput

echo "Starting Gunicorn..."
gunicorn backend.wsgi:application --bind 0.0.0.0:8000 &

echo "Starting Celery worker..."
celery -A backend.celery_app worker -l info &

# Delay Celery Beat until migrations are applied
sleep 5
echo "Starting Celery Beat..."
celery -A backend.celery_app beat -l info --scheduler django_celery_beat.schedulers:DatabaseScheduler
