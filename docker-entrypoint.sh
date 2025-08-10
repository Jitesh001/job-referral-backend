#!/usr/bin/env bash
set -euo pipefail

python manage.py migrate --noinput

# Forward signals to children and exit when they do
term_handler() {
  echo "Shutting down..."
  kill -TERM "$GUNICORN_PID" 2>/dev/null || true
  kill -TERM "$CELERYW_PID" 2>/dev/null || true
  kill -TERM "$CELERYB_PID" 2>/dev/null || true
  wait
}
trap term_handler SIGTERM SIGINT

# Start Gunicorn
gunicorn backend.wsgi:application --bind 0.0.0.0:${PORT:-8000} &
GUNICORN_PID=$!

# EITHER: start worker + beat as separate processes (recommended)
celery -A backend.celery_app worker -l info &
CELERYW_PID=$!

celery -A backend.celery_app beat -l info \
  --scheduler django_celery_beat.schedulers:DatabaseScheduler &
CELERYB_PID=$!

wait
