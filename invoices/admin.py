from django.contrib import admin

from .models import Invoice, InvoiceItem


class InvoiceItemInline(admin.TabularInline):
    model = InvoiceItem
    extra = 1


@admin.register(Invoice)
class InvoiceAdmin(admin.ModelAdmin):
    list_display = (
        "invoice_number",
        "client",
        "invoice_date",
        "grand_total",
        "payment_status",
        "payment_method",
        "created_by",
    )
    list_filter = (
        "payment_status",
        "payment_method",
        "invoice_date",
    )
    search_fields = (
        "invoice_number",
        "client__name",
        "client__phone_number",
    )
    readonly_fields = ("created_at", "updated_at")
    list_select_related = ("client", "created_by")
    inlines = [InvoiceItemInline]


@admin.register(InvoiceItem)
class InvoiceItemAdmin(admin.ModelAdmin):
    list_display = (
        "invoice",
        "paint",
        "quantity",
        "unit_price",
        "gst_percentage",
        "line_discount",
        "line_total",
    )
    search_fields = (
        "invoice__invoice_number",
        "paint__name",
    )