from django.db import models
from core.models import TimeStampModel


class Subject(TimeStampModel):
    group_id = models.ForeignKey(
        "groups.Group", related_name="group", on_delete=models.CASCADE
    )
    time = models.IntegerField(default=1)
    title = models.CharField(max_length=300)
    description = models.TextField(max_length=1000, blank=True, null=True)
    writer = models.ForeignKey(
        "users.User",
        related_name="subject_writer",
        blank=False,
        null=False,
        on_delete=models.CASCADE,
    )

    def __str__(self):
        return f"Subject [{self.title}]"


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
    progress = models.CharField(
        choices=PROGRESS_CHOICES, default=PROGRESS_CREATE, max_length=20
    )
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
    start = models.DateTimeField(blank=False, null=False)
    end = models.DateTimeField(blank=False, null=False)

    def __str__(self):
        return f"TodoGroup [{self.title}]"


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
    start = models.DateTimeField(blank=False, null=False)
    end = models.DateTimeField(blank=False, null=False)

    def __str__(self):
        return f"Todo [{self.title}]"