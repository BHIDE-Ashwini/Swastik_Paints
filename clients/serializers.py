from rest_framework import serializers

from .models import Client


class ClientSerializer(serializers.ModelSerializer):
    class Meta:
        model = Client
        fields = [
            "id",
            "name",
            "phone_number",
            "email",
            "address",
            "city",
            "state",
            "pin_code",
            "gst_number",
            "registration_date",
            "created_at",
            "updated_at",
        ]
        read_only_fields = [
            "id",
            "registration_date",
            "created_at",
            "updated_at",
        ]