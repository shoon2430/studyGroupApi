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

    list_display = ("title", "writer", "time")


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
                )
            },
        ),
    )

    fieldsets = COSTOM_FIELDS

    list_display = (
        "title",
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
                    "writer",
                )
            },
        ),
    )

    fieldsets = COSTOM_FIELDS

    list_display = ("title", "writer", "time")
