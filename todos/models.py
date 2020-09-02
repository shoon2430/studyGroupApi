from django.db import models
from core.models import TimeStampModel


class Subject(TimeStampModel):
    group_id = models.ForeignKey(
        "groups.Group",
        blank=False,
        null=False,
        on_delete=models.CASCADE,
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


class Todo(TimeStampModel):
    PROGRESS_CREATE = "CREATE"
    PROGRESS_DOING = "DOING"
    PROGRESS_COMPLETED = "COMPLETED"

    PROGRESS_CHOICES = [
        (PROGRESS_CREATE, "Create"),
        (PROGRESS_DOING, "Doing"),
        (PROGRESS_COMPLETED, "Completed"),
    ]

    subject_id = models.ForeignKey(
        "todos.Subject",
        blank=False,
        null=False,
        on_delete=models.CASCADE,
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
