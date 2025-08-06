import logging

from django.conf import settings


class RequireMailTrue(logging.Filter):
    def filter(self, record):
        return getattr(settings, "ENABLE_ADMIN_EMAIL", True)
