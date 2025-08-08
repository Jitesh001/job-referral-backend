#!/bin/bash

# Wait for DB to be ready (optional but recommended)
echo "Waiting for PostgreSQL to be ready..."
until pg_isready -h "$DB_HOST" -p "$DB_PORT" -U "$POSTGRES_USER"; do
  sleep 1
done

# Apply database migrations
echo "Applying database migrations"
python manage.py migrate

# Collect static files
echo "Running collect static"
python manage.py collectstatic --noinput

# Start all processes
echo "Starting server"
gunicorn backend.wsgi:application --bind 0.0.0.0:8000 &

echo "Starting Celery worker"
celery -A backend.celery_app worker -l info &

echo "Starting Celery beat"
celery -A backend.celery_app beat -l info --scheduler django_celery_beat.schedulers:DatabaseScheduler
