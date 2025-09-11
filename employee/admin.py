from django.contrib import admin
from .models import Position, Employee


@admin.register(Position)
class PositionAdmin(admin.ModelAdmin):
    list_display = ("name", "full_name", "code", "organization", "created_at")
    list_filter = ("organization",)
    search_fields = ("name", "full_name", "code")


@admin.register(Employee)
class EmployeeAdmin(admin.ModelAdmin):
    list_display = (
        "name",
        "organization",
        "from_date",
        "to_date",
        "created_at",
    )
    list_filter = ("organization", "department", "position")
    search_fields = ("name",)
