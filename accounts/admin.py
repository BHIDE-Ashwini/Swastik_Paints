from django.contrib import admin

from .models import Admin


@admin.register(Admin)
class AdminAdmin(admin.ModelAdmin):
    list_display = (
        "full_name",
        "phone_number",
        "role",
        "is_active",
        "last_login",
        "created_at",
    )
    list_filter = ("role", "is_active")
    search_fields = (
        "full_name",
        "phone_number",
        "user__username",
        "user__email",
    )
    readonly_fields = ("created_at", "updated_at", "last_login")