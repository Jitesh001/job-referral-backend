#!/bin/bash

set -e  # Exit if any command fails

echo "Running database migrations..."
python manage.py migrate

echo "Starting Gunicorn..."
exec gunicorn backend.wsgi:application --bind 0.0.0.0:8000
