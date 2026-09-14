from rest_framework import serializers

from .models import DeliveryChallan, DeliveryChallanItem


class DeliveryChallanItemSerializer(serializers.ModelSerializer):
    paint_name = serializers.CharField(
        source="paint.name",
        read_only=True,
    )

    class Meta:
        model = DeliveryChallanItem
        fields = [
            "id",
            "paint",
            "paint_name",
            "description",
            "hsn_sac_code",
            "batch_number",
            "pack_description",
            "quantity",
            "created_at",
        ]
        read_only_fields = [
            "id",
            "paint_name",
            "created_at",
        ]


class DeliveryChallanSerializer(serializers.ModelSerializer):
    items = DeliveryChallanItemSerializer(many=True)

    client_name = serializers.CharField(
        source="client.name",
        read_only=True,
    )
    created_by = serializers.PrimaryKeyRelatedField(
        read_only=True,
    )

    class Meta:
        model = DeliveryChallan
        fields = [
            "id",
            "challan_number",
            "challan_date",
            "client",
            "client_name",
            "created_by",
            "po_number",
            "classification",
            "shipping_name",
            "shipping_address",
            "shipping_city",
            "shipping_state",
            "shipping_pin_code",
            "shipping_gst_number",
            "eway_bill_number",
            "removal_date",
            "removal_time",
            "dispatched_through",
            "vehicle_number",
            "lr_number",
            "lr_date",
            "notes",
            "items",
            "created_at",
            "updated_at",
        ]
        read_only_fields = [
            "id",
            "client_name",
            "created_by",
            "created_at",
            "updated_at",
        ]

    def create(self, validated_data):
        items_data = validated_data.pop("items")
        request = self.context["request"]

        try:
            admin = request.user.admin_profile
        except AttributeError:
            raise serializers.ValidationError(
                {"detail": "An active admin profile is required."}
            )

        if not admin.is_active:
            raise serializers.ValidationError(
                {"detail": "An active admin profile is required."}
            )

        challan = DeliveryChallan.objects.create(
            created_by=admin,
            **validated_data,
        )

        DeliveryChallanItem.objects.bulk_create(
            [
                DeliveryChallanItem(
                    delivery_challan=challan,
                    **item_data,
                )
                for item_data in items_data
            ]
        )

        return challan

    def update(self, instance, validated_data):
        items_data = validated_data.pop("items", None)

        for field, value in validated_data.items():
            setattr(instance, field, value)

        instance.save()

        if items_data is not None:
            instance.items.all().delete()

            DeliveryChallanItem.objects.bulk_create(
                [
                    DeliveryChallanItem(
                        delivery_challan=instance,
                        **item_data,
                    )
                    for item_data in items_data
                ]
            )

        return instance