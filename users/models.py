import uuid
from django.db import models
from django.contrib.auth.models import AbstractUser


class User(AbstractUser):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    avatar = models.ImageField(upload_to="avatars", null=True, blank=True)
    nickname = models.CharField(blank=False, max_length=100)
    phone = models.CharField(blank=False, default="010-0000-0000", max_length=13)
    introduce = models.TextField(max_length=300, blank=True, default="")
    attendGroups = models.ManyToManyField(
        "groups.Group", related_name="groups", blank=True
    )

    def __str__(self):
        return self.username
