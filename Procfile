release: python manage.py migrate
web: gunicorn backend.wsgi:application --bind 0.0.0.0:8000
worker: celery -A backend.celery_app worker -l info
beat: celery -A backend.celery_app beat -l info --scheduler django_celery_beat.schedulers:DatabaseScheduler
