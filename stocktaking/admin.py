from django.contrib import admin
from .models import Stocktaking, Inspection


class InspectionInline(admin.TabularInline):
    """
    Display Inspection records inside Stocktaking admin
    in a compact table layout.
    """
    model = Inspection
    extra = 1                     # how many blank rows to show
    readonly_fields = ("created_at",)  # created_at is auto-set


@admin.register(Stocktaking)
class StocktakingAdmin(admin.ModelAdmin):
    list_display = (
        "number",
        "inventory",
        "employee",
        "date",
        "terminate_date",
        "created_at",
    )
    list_filter = ("inventory__organization", "date")
    search_fields = ("number",)
    inlines = [InspectionInline]   # Attach the inline here


@admin.register(Inspection)
class InspectionAdmin(admin.ModelAdmin):
    """
    Optional separate admin for Inspection if you also want
    to browse all inspections independently.
    """
    list_display = ("id", "stocktaking", "user", "created_at")
    list_filter = ("created_at",)
    search_fields = ("id", "stocktaking__number")
