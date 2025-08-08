#!/bin/bash

set -e  # Exit if any command fails

echo "---- ENV DEBUG ----"
echo "DATABASE_URL = $DATABASE_URL"
echo "--------------------"


echo "Running database migrations..."
python manage.py migrate

echo "Starting Gunicorn..."
exec gunicorn backend.wsgi:application --bind 0.0.0.0:8000

echo "Current settings:"
python -c "from django.conf import settings; print(settings.DATABASES)"
