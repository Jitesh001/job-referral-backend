#!/bin/bash

set -e  # Exit if any command fails

echo "---- ENV DEBUG ----"
echo "DATABASE_URL = $DATABASE_URL"
echo "--------------------"

echo "Starting Gunicorn..."
exec gunicorn backend.wsgi:application --bind 0.0.0.0:8000
