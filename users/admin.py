from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import User


@admin.register(User)
class UserAdmin(admin.ModelAdmin):

    COSTOM_FIELDS = (
        (
            ("CostomFields"),
            {
                "fields": (
                    "username",
                    "password",
                    "avatar",
                    "nickname",
                    "email",
                    "phone",
                )
            },
        ),
        (("Important dates"), {"fields": ("last_login", "date_joined")}),
        (
            ("Permissions"),
            {
                "fields": (
                    "is_active",
                    "is_staff",
                    "is_superuser",
                    "user_permissions",
                )
            },
        ),
    )

    fieldsets = COSTOM_FIELDS

    list_display = (
        "username",
        "nickname",
        "email",
        "date_joined",
    )

    # 필터는 일단 보류
    # list_filter = UserAdmin.list_filter
