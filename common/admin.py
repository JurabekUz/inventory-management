from django.contrib import admin

from . import models


@admin.register(models.Department)
class DepartmentAdmin(admin.ModelAdmin):
    list_display = ('name', 'code', 'organization')
    list_filter = ('organization',)


class InventoryGroupInline(admin.TabularInline):
    model = models.InventoryGroup
    fields = ('name', 'code')
    readonly_fields = ('code', 'name')
    extra = 0
    can_delete = False

    def has_add_permission(self, request, obj):
        return False


@admin.register(models.InventoryGroup)
class InventoryGroupAdmin(admin.ModelAdmin):
    list_display = ('name', 'code', 'organization', 'parent')
    list_filter = ('organization',)
    readonly_fields = ['code']
    inlines = [InventoryGroupInline]


