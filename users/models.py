from django.contrib.auth.models import AbstractUser
from django.db import models

class User(AbstractUser):
    telegram_id = models.CharField()

    USERNAME_FIELD = "telegram_id"
    REQUIRED_FIELDS = ["telegram_id"]