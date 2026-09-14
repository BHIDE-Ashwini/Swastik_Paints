from rest_framework import serializers

from .models import Category, Paint, PaintImage


class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = [
            "id",
            "name",
            "parent",
        ]
        read_only_fields = ["id"]


class PaintImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = PaintImage
        fields = [
            "id",
            "image",
            "is_primary",
            "created_at",
        ]
        read_only_fields = [
            "id",
            "created_at",
        ]


class PaintSerializer(serializers.ModelSerializer):
    images = PaintImageSerializer(
        many=True,
        read_only=True,
    )

    class Meta:
        model = Paint
        fields = [
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
            "description",
            "is_available",
            "images",
            "created_at",
            "updated_at",
        ]
        read_only_fields = [
            "id",
            "images",
            "created_at",
            "updated_at",
        ]