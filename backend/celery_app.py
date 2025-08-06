import os

from celery import Celery
from celery.signals import setup_logging  # noqa

# set the default Django settings module for the 'celery' program.
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "backend.settings")

app = Celery("backend")
app.config_from_object("django.conf:settings", namespace="CELERY")
app.conf.update({"worker_hijack_root_logger": False})


@setup_logging.connect
def config_loggers(*args, **kwargs):
    from logging.config import dictConfig  # noqa

    from django.conf import settings  # noqa

    dictConfig(settings.LOGGING)


# Load task modules from all registered Django app configs.
app.autodiscover_tasks()


@app.task(bind=True)
def debug_task(self):
    from celery.utils.log import get_task_logger  # noqa

    logger = get_task_logger(__name__)
    logger.info(f"Request: {self.request}")
