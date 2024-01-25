from django.db import models
from django.contrib.auth.models import AbstractUser

class LinkerUser(AbstractUser):
    quote = models.TextField(
        blank=True,
        null=True,
        max_length=300,
    )
    birth_date = models.DateField(
        blank=True,
        null=True,
    )