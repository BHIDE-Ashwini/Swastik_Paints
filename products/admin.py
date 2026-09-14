from django.contrib import admin

from .models import Category, Paint, PaintImage


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ["id", "name", "parent"]
    search_fields = ["name"]


@admin.register(Paint)
class PaintAdmin(admin.ModelAdmin):
    list_display = [
        "id",
        "name",
        "category",
        "finish",
        "color",
        "shade_code",
        "size",
        "price",
        "gst_percentage",
        "hsn_sac_code",
        "is_available",
    ]
    list_filter = [
        "category",
        "finish",
        "is_available",
    ]
    search_fields = [
        "name",
        "color",
        "shade_code",
        "hsn_sac_code",
    ]


@admin.register(PaintImage)
class PaintImageAdmin(admin.ModelAdmin):
    list_display = [
        "id",
        "paint",
        "is_primary",
        "created_at",
    ]
    list_filter = ["is_primary"]
    search_fields = ["paint__name"]