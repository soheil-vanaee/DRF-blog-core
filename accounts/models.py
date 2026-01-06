from django.db import models
from django.contrib.auth.models import AbstractUser
from django.utils import timezone


class CustomUser(AbstractUser):
    email = models.EmailField(unique=True)
    ip_address = models.GenericIPAddressField(null=True, blank=True)  # Store IP address
    account_creation_date = models.DateTimeField(default=timezone.now)  # Store account creation date
    last_login_date = models.DateTimeField(null=True, blank=True)  # Store last login date

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username']

    def __str__(self):
        return self.email
