from django.db import models
from django.contrib.auth.models import AbstractUser


class User(AbstractUser):

    name = models.CharField(blank=False, max_length=100)
    phone = models.CharField(blank=False, default="010-0000-0000", max_length=13)
    avatar = models.ImageField(upload_to="avatars", null=True, blank=True)

    def __str__(self):
        return self.username
