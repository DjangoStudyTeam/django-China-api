from django.contrib import admin
from django.contrib.auth import admin as auth_admin
from django.utils.translation import gettext_lazy as _

from .models import User


@admin.register(User)
class UserAdmin(auth_admin.UserAdmin):
    fieldsets = (
        ("User", {"fields": ("nickname", "avatar")}),
        (None, {"fields": ("username", "password")}),
        (_("Personal info"), {"fields": ("first_name", "last_name", "email")}),
        (
            _("Permissions"),
            {
                "fields": (
                    "is_active",
                    "is_staff",
                    "is_superuser",
                    "groups",
                    "user_permissions",
                ),
            },
        ),
        (_("Important dates"), {"fields": ("last_login", "date_joined")}),
    )
    list_display = ["id", "username", "nickname", "is_superuser", "is_active"]
    search_fields = ["username", "nickname", "email"]
