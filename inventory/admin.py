from django.contrib import admin

from .models import Stock, StockMovement


@admin.register(Stock)
class StockAdmin(admin.ModelAdmin):
    list_display = (
        "paint",
        "quantity",
        "low_stock_threshold",
        "updated_at",
    )
    search_fields = (
        "paint__name",
        "paint__shade_code",
    )
    readonly_fields = ("updated_at",)
    list_select_related = ("paint",)


@admin.register(StockMovement)
class StockMovementAdmin(admin.ModelAdmin):
    list_display = (
        "paint",
        "movement_type",
        "quantity",
        "reference_invoice",
        "created_at",
    )
    list_filter = ("movement_type",)
    search_fields = (
        "paint__name",
        "reference_invoice__invoice_number",
    )
    readonly_fields = ("created_at",)
    list_select_related = ("paint", "reference_invoice")