from django.contrib import admin
from .models import Subject, Todo, TodoGroup


@admin.register(Subject)
class SubjectAdmin(admin.ModelAdmin):
    COSTOM_FIELDS = (
        (
            ("SubjectInfo"),
            {
                "fields": (
                    "group_id",
                    "title",
                    "description",
                    "writer",
                    "time",
                )
            },
        ),
    )

    fieldsets = COSTOM_FIELDS

    list_display = ("title", "group_id", "writer", "time")


@admin.register(TodoGroup)
class TodoGroupAdmin(admin.ModelAdmin):
    COSTOM_FIELDS = (
        (
            ("TodoGroupInfo"),
            {
                "fields": (
                    "subject_id",
                    "time",
                    "title",
                    "progress",
                    "leader",
                    "members",
                    "start",
                    "end",
                )
            },
        ),
    )

    fieldsets = COSTOM_FIELDS

    list_display = (
        "title",
        "subject_id",
        "leader",
        "time",
    )


@admin.register(Todo)
class TodoAdmin(admin.ModelAdmin):

    COSTOM_FIELDS = (
        (
            ("TodoInfo"),
            {
                "fields": (
                    "todoGroup_id",
                    "time",
                    "title",
                    "progress",
                    "writer",
                    "start",
                    "end",
                )
            },
        ),
    )

    fieldsets = COSTOM_FIELDS

    list_display = ("title", "todoGroup_id", "writer", "time")
