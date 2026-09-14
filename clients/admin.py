from django.contrib import admin

from .models import Client


@admin.register(Client)
class ClientAdmin(admin.ModelAdmin):
    list_display = (
        "name",
        "phone_number",
        "email",
        "city",
        "state",
        "gst_number",
        "registration_date",
    )
    search_fields = (
        "name",
        "phone_number",
        "email",
        "gst_number",
    )
    list_filter = ("state", "city")
    readonly_fields = ("registration_date", "created_at", "updated_at")