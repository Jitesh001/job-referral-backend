import logging

from django.conf import settings
from django.template.loader import render_to_string

from backend.celery_app import app
from backend.utils import send_email
from jobs.models import User

logger = logging.getLogger(__name__)


@app.task(bind=True)
def send_otp_email(_, user_uuid, otp):
    try:
        User.objects.get(uuid=user_uuid)
    except User.DoesNotExist:
        logger.error(f"User with UUID {user_uuid} does not exist.")
        return

    subject = "Your OTP Code"
    template = "emails/test_email.html"
    msg_html = render_to_string(
        template,
        {
            "sample_message": f"Your OTP code is: {otp}. Please use this code to verify your account.",
        },
    ).strip()

    send_email(
        subject=subject,
        body=msg_html,
        from_email=settings.DEFAULT_FROM_EMAIL,
        to=[settings.MAIL_TO],
        alternatives=[(msg_html, "text/html")],
    )


@app.task(bind=True)
def sent_test_email(_):
    subject = "test email"
    template = "emails/test_email.html"
    msg_html = render_to_string(
        template,
        {
            "sample_message": "This is test email XD....",
        },
    ).strip()
    email = "jiteshshewale40@gmail.com"

    send_email(
        subject=subject,
        body=msg_html,
        from_email=settings.DEFAULT_FROM_EMAIL,
        to=[email],
        alternatives=[(msg_html, "text/html")],
    )
