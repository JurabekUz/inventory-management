from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.utils.translation import gettext_lazy as _

from .models import User


@admin.register(User)
class UserAdmin(UserAdmin):
    list_display = ['username', 'org', 'first_name', 'last_name', 'email']
    list_filter = ['org']
    fieldsets = (
        (None, {"fields": ("username", "password")}),
        (_("Personal info"), {"fields": ("first_name", "last_name", "email", "org")}),
        (
            _("Permissions"),
            {
                "fields": (
                    "is_active",
                    # "is_staff",
                    # "is_superuser",
                    # "groups",
                    # "user_permissions",
                ),
            },
        )
    )