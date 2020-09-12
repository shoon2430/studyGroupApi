from django.db import models
from core.models import TimeStampModel


class Subject(TimeStampModel):
    group_id = models.ForeignKey(
        "groups.Group", related_name="group", on_delete=models.CASCADE
    )
    time = models.IntegerField(default=1)
    title = models.CharField(max_length=300)
    writer = models.ForeignKey(
        "users.User",
        related_name="subject_writer",
        blank=False,
        null=False,
        on_delete=models.CASCADE,
    )


class TodoGroup(TimeStampModel):
    PROGRESS_CREATE = "CREATE"
    PROGRESS_DOING = "DOING"
    PROGRESS_COMPLETED = "COMPLETED"

    PROGRESS_CHOICES = [
        (PROGRESS_CREATE, "Create"),
        (PROGRESS_DOING, "Doing"),
        (PROGRESS_COMPLETED, "Completed"),
    ]

    subject_id = models.ForeignKey(
        "Subject", related_name="subject", on_delete=models.CASCADE
    )
    time = models.IntegerField(default=1)
    title = models.CharField(max_length=300)
    progress = models.CharField(choices=PROGRESS_CHOICES, max_length=20)
    leader = models.ForeignKey(
        "users.User",
        related_name="todo_Leader",
        blank=False,
        null=False,
        on_delete=models.CASCADE,
    )
    members = models.ManyToManyField(
        "users.User", related_name="todo_members", blank=True
    )


class Todo(TimeStampModel):
    PROGRESS_CREATE = "CREATE"
    PROGRESS_DOING = "DOING"
    PROGRESS_COMPLETED = "COMPLETED"

    PROGRESS_CHOICES = [
        (PROGRESS_CREATE, "Create"),
        (PROGRESS_DOING, "Doing"),
        (PROGRESS_COMPLETED, "Completed"),
    ]

    todoGroup_id = models.ForeignKey(
        "TodoGroup", related_name="todo_group", on_delete=models.CASCADE
    )
    time = models.IntegerField(default=1)
    title = models.CharField(max_length=300)
    progress = models.CharField(choices=PROGRESS_CHOICES, max_length=20)
    writer = models.ForeignKey(
        "users.User",
        related_name="todo_writer",
        blank=False,
        null=False,
        on_delete=models.CASCADE,
    )
