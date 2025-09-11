from django.contrib import admin

from .models import Organization


@admin.register(Organization)
class OrganizationAdmin(admin.ModelAdmin):
    list_display = ("name", 'code', 'type', 'register_number', 'register_date', 'created_at')
    search_fields = ("name", 'code', 'register_number')

