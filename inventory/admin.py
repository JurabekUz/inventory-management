from django.contrib import admin
from .models import Inventory


@admin.register(Inventory)
class InventoryAdmin(admin.ModelAdmin):
    list_display = (
        "name",
        "organization",
        "contract",
        "amount",
        "price",
        "total_value",
        "date",
        "terminate_date",
        "created_at",
    )
    list_filter = (
        "organization",
        "group",
        "type",
        "contract",
        "measure_unit",
        "qqs",
        "date",
    )
    search_fields = ("name", "full_name", "code")
    readonly_fields = ("code",)  # code is editable=False

    # Optional: order by date descending in admin
    ordering = ("-date",)
