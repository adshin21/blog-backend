from django.db import models
from django.contrib.auth.models import AbstractUser
# Create your models here.


class User(AbstractUser):
    email = models.EmailField(unique=True, blank=False)
    provider = models.CharField(blank=True, max_length=200)
    # is_active = models.BooleanField(default=False)
    REQUIRED_FIELDS = ["email"]

    def __str__(self):
        return self.username + ' ' + self.email
