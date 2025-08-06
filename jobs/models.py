from datetime import datetime, timedelta
from typing import List

import pyotp
from django.contrib.auth.models import AbstractUser
from django.contrib.postgres.fields import ArrayField
from django.db import models
from django.utils import timezone
from django.utils.translation import gettext_lazy as _

from . import managers
from .mixins import AbstractTrack


class User(AbstractUser, AbstractTrack):
    full_name = models.CharField(max_length=50)
    email = models.EmailField(
        _("email address"),
        unique=True,
    )
    phone_number = models.CharField(max_length=10, null=True, blank=True)
    is_verified = models.BooleanField(default=False)
    otp_secret = models.CharField(max_length=32, blank=True, null=True)
    otp_created_at = models.DateTimeField(blank=True, null=True)

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS: List[str] = []
    manager = managers.UserManager()

    def save(self, *args, **kwargs):
        self.username = self.email.lower()
        if not self.full_name:
            self.full_name = f"{self.first_name} {self.last_name}"
        if self.email:
            self.email = self.email.lower()
        super().save(*args, **kwargs)

    def __str__(self):
        return self.email

    def generate_otp(self):
        """Generate a new OTP for the user"""
        if not self.otp_secret:
            self.otp_secret = pyotp.random_base32()
            self.save()

        totp = pyotp.TOTP(self.otp_secret, interval=60)
        self.otp_created_at = datetime.now()
        self.save()
        return totp.now()

    def verify_otp(self, otp):
        """Verify the provided OTP"""
        if not self.otp_secret or not self.otp_created_at:
            return False

        # Check if OTP is expired (1 minutes)
        if timezone.now() > self.otp_created_at + timedelta(minutes=1):
            return False

        totp = pyotp.TOTP(self.otp_secret, interval=60)  # 1-minutes interval
        return totp.verify(otp)


class JobPost(AbstractTrack):
    class JobTypeChoices(models.TextChoices):
        FULL_TIME = "FULL_TIME", "Full Time"
        PART_TIME = "PART_TIME", "Part Time"
        CONTRACT = "CONTRACT", "Contract"
        INTERNSHIP = "INTERNSHIP", "Internship"
        FREELANCE = "FREELANCE", "Freelance"
        TEMPORARY = "TEMPORARY", "Temporary"

    class JobModeChoices(models.TextChoices):
        WORK_FROM_OFFICE = "WORK_FROM_OFFICE", "Work from Office"
        WORK_FROM_HOME = "WORK_FROM_HOME", "Work from Home"
        HYBRID = "HYBRID", "Hybrid"

    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="job_posts")
    job_title = models.CharField(max_length=255)
    company_name = models.CharField(max_length=255)
    company_link = models.URLField(blank=True, null=True)
    job_type = ArrayField(
        models.CharField(max_length=20, choices=JobTypeChoices.choices),
        default=list,
        blank=True,
    )
    job_mode = ArrayField(
        models.CharField(max_length=20, choices=JobModeChoices.choices),
        default=list,
        blank=True,
    )
    job_location = ArrayField(
        models.CharField(max_length=255),
        default=list,
        blank=True,
    )
    contact_emails = ArrayField(
        models.EmailField(),
        default=list,
        blank=True,
    )
    contact_phones = ArrayField(
        models.CharField(max_length=10),
        default=list,
        blank=True,
    )
    job_description = models.TextField()

    def __str__(self):
        return f"{self.title} at {self.company_name}"
