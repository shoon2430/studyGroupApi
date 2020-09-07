from django.contrib import admin
from .models import Subject, Todo


@admin.register(Subject)
class SubjectAdmin(admin.ModelAdmin):

    COSTOM_FIELDS = (
        (
            ("SubjectInfo"),
            {
                "fields": (
                    "group_id",
                    "title",
                    "writer",
                    "time",
                )
            },
        ),
    )

    fieldsets = COSTOM_FIELDS

    list_display = ("group_id", "title", "writer", "time")


@admin.register(Todo)
class TodoAdmin(admin.ModelAdmin):

    COSTOM_FIELDS = (
        (
            ("TodoInfo"),
            {
                "fields": (
                    "subject_id",
                    "time",
                    "title",
                    "writer",
                )
            },
        ),
    )

    fieldsets = COSTOM_FIELDS

    list_display = ("subject_id", "title", "writer", "time")
