from django.contrib import admin
from .models import Group


@admin.register(Group)
class GroupAdmin(admin.ModelAdmin):

    COSTOM_FIELDS = (
        (
            ("GroupInfo"),
            {"fields": ("photo", "category", "title", "time")},
        ),
        (("GroupInfo users"), {"fields": ("leader", "members", "attends")}),
    )

    fieldsets = COSTOM_FIELDS

    list_display = ("title", "category", "time", "leader")
