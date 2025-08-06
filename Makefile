# target: createapp - Create a new Django app. Usage: make createapp app=app1
createapp:
	python manage.py startapp $(app)

# target: makemigrations - Create new migrations
makemigrations:
	python manage.py makemigrations

# Add others as needed
migrate:
	python manage.py migrate

run:
	python manage.py runserver

# target: freeze - Freeze installed packages to requirements.txt
freeze:
	pip freeze > requirements.txt


# target: sh - open django extension's shell plus
sh:
	python manage.py shell_plus

# target: db - open django DB shell
db:
	python manage.py dbshell


# target: celery - Run the Celery worker with beat and DB scheduler
celery:
	celery -A backend worker -l info --beat --scheduler django_celery_beat.schedulers:DatabaseScheduler

# target: celery_dev - Auto-restarts the Celery worker on code changes
celery_dev:
	watchmedo auto-restart -d . -p "*.py" --recursive -- \
	celery -A backend worker -l info --beat --scheduler django_celery_beat.schedulers:DatabaseScheduler
