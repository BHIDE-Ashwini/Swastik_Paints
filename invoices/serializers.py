from decimal import Decimal, ROUND_HALF_UP

from django.db import transaction
from rest_framework import serializers

from .models import (
    DeliveryChallan,
    DeliveryChallanItem,
    Invoice,
    InvoiceItem,
)


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


class InvoiceItemSerializer(serializers.ModelSerializer):
    paint_name = serializers.CharField(
        source="paint.name",
        read_only=True,
    )

    class Meta:
        model = InvoiceItem
        fields = [
            "id",
            "paint",
            "paint_name",
            "description",
            "hsn_sac_code",
            "batch_number",
            "pack_description",
            "quantity",
            "unit_price",
            "gst_percentage",
            "line_discount",
            "line_total",
        ]
        read_only_fields = [
            "id",
            "paint_name",
            "description",
            "hsn_sac_code",
            "gst_percentage",
            "line_total",
        ]

    def validate_unit_price(self, value):
        if value < 0:
            raise serializers.ValidationError(
                "Unit price cannot be negative."
            )

        return value


class InvoiceSerializer(serializers.ModelSerializer):
    items = InvoiceItemSerializer(many=True)

    client_name = serializers.CharField(
        source="client.name",
        read_only=True,
    )

    created_by = serializers.PrimaryKeyRelatedField(
        read_only=True,
    )

    delivery_challans = serializers.PrimaryKeyRelatedField(
        many=True,
        queryset=DeliveryChallan.objects.all(),
        required=False,
    )

    class Meta:
        model = Invoice
        fields = [
            "id",
            "invoice_number",
            "invoice_date",
            "client",
            "client_name",
            "created_by",
            "delivery_challans",

            # Document details
            "po_number",
            "payment_terms",
            "classification",
            "eway_bill_number",
            "removal_date",
            "removal_time",
            "dispatched_through",
            "vehicle_number",
            "lr_number",
            "lr_date",

            # Billing snapshot
            "billing_name",
            "billing_phone",
            "billing_email",
            "billing_address",
            "billing_city",
            "billing_state",
            "billing_pin_code",
            "billing_gst_number",

            # Shipping snapshot
            "shipping_name",
            "shipping_address",
            "shipping_city",
            "shipping_state",
            "shipping_pin_code",

            # GST and totals
            "gst_type",
            "subtotal",
            "discount_amount",
            "taxable_amount",
            "cgst_amount",
            "sgst_amount",
            "igst_amount",
            "gst_amount",
            "additional_charges",
            "round_off",
            "grand_total",

            # Payment
            "payment_status",
            "payment_method",
            "notes",
            "pdf_file",

            # Items
            "items",

            "created_at",
            "updated_at",
        ]

        read_only_fields = [
            "id",
            "client_name",
            "created_by",

            # Historical billing snapshot
            "billing_name",
            "billing_phone",
            "billing_email",
            "billing_address",
            "billing_city",
            "billing_state",
            "billing_pin_code",
            "billing_gst_number",

            # Server-calculated values
            "subtotal",
            "discount_amount",
            "taxable_amount",
            "cgst_amount",
            "sgst_amount",
            "igst_amount",
            "gst_amount",
            "round_off",
            "grand_total",

            "created_at",
            "updated_at",
        ]

    def validate(self, attrs):
        client = attrs.get("client")

        if self.instance:
            client = client or self.instance.client

            if (
                "client" in attrs
                and client != self.instance.client
            ):
                raise serializers.ValidationError(
                    {
                        "client": (
                            "The client cannot be changed after "
                            "the invoice has been created."
                        )
                    }
                )

        if client is None:
            raise serializers.ValidationError(
                {"client": "Client is required."}
            )

        delivery_challans = attrs.get("delivery_challans")

        if delivery_challans is None and self.instance:
            delivery_challans = list(
                self.instance.delivery_challans.all()
            )

        if delivery_challans:
            challan_client_ids = {
                challan.client_id
                for challan in delivery_challans
            }

            if challan_client_ids != {client.id}:
                raise serializers.ValidationError(
                    {
                        "delivery_challans": (
                            "All delivery challans must belong "
                            "to the selected client."
                        )
                    }
                )

            already_invoiced = []

            for challan in delivery_challans:
                if self.instance:
                    already_linked = challan.invoices.exclude(
                        pk=self.instance.pk
                    ).exists()
                else:
                    already_linked = challan.invoices.exists()

                if already_linked:
                    already_invoiced.append(
                        challan.challan_number
                    )

            if already_invoiced:
                raise serializers.ValidationError(
                    {
                        "delivery_challans": (
                            "These delivery challans are already "
                            "linked to another invoice: "
                            f"{', '.join(already_invoiced)}."
                        )
                    }
                )

        return attrs

    def _calculate_item(self, item):
        quantity = Decimal(item["quantity"])
        unit_price = item["unit_price"]

        line_discount = item.get(
            "line_discount",
            Decimal("0.00"),
        )

        gst_percentage = item["gst_percentage"]

        gross_amount = quantity * unit_price
        taxable_amount = gross_amount - line_discount

        if taxable_amount < 0:
            raise serializers.ValidationError(
                "Line discount cannot exceed the line amount."
            )

        gst_amount = (
            taxable_amount
            * gst_percentage
            / Decimal("100")
        )

        return (
            gross_amount.quantize(Decimal("0.01")),
            taxable_amount.quantize(Decimal("0.01")),
            gst_amount.quantize(Decimal("0.01")),
        )

    def _calculate_totals(
        self,
        items,
        gst_type,
        additional_charges,
    ):
        subtotal = Decimal("0.00")
        discount_amount = Decimal("0.00")
        taxable_amount = Decimal("0.00")
        gst_amount = Decimal("0.00")

        for item in items:
            gross, taxable, gst = self._calculate_item(item)

            subtotal += gross

            discount_amount += item.get(
                "line_discount",
                Decimal("0.00"),
            )

            taxable_amount += taxable
            gst_amount += gst

        if gst_type == Invoice.GSTType.INTRA_STATE:
            cgst_amount = gst_amount / Decimal("2")
            sgst_amount = gst_amount - cgst_amount
            igst_amount = Decimal("0.00")

        elif gst_type == Invoice.GSTType.INTER_STATE:
            cgst_amount = Decimal("0.00")
            sgst_amount = Decimal("0.00")
            igst_amount = gst_amount

        else:
            raise serializers.ValidationError(
                {"gst_type": "GST type is required."}
            )

        total_before_rounding = (
            taxable_amount
            + gst_amount
            + additional_charges
        )

        rounded_total = total_before_rounding.quantize(
            Decimal("1"),
            rounding=ROUND_HALF_UP,
        )

        round_off = rounded_total - total_before_rounding

        return {
            "subtotal": subtotal.quantize(
                Decimal("0.01")
            ),
            "discount_amount": discount_amount.quantize(
                Decimal("0.01")
            ),
            "taxable_amount": taxable_amount.quantize(
                Decimal("0.01")
            ),
            "cgst_amount": cgst_amount.quantize(
                Decimal("0.01")
            ),
            "sgst_amount": sgst_amount.quantize(
                Decimal("0.01")
            ),
            "igst_amount": igst_amount.quantize(
                Decimal("0.01")
            ),
            "gst_amount": gst_amount.quantize(
                Decimal("0.01")
            ),
            "round_off": round_off.quantize(
                Decimal("0.01")
            ),
            "grand_total": rounded_total.quantize(
                Decimal("0.01")
            ),
        }

    def _client_billing_snapshot(self, client):
        return {
            "billing_name": client.name,
            "billing_phone": client.phone_number,
            "billing_email": client.email,
            "billing_address": client.address,
            "billing_city": client.city,
            "billing_state": client.state,
            "billing_pin_code": client.pin_code,
            "billing_gst_number": client.gst_number,
        }

    def _default_shipping_snapshot(self, client):
        return {
            "shipping_name": client.name,
            "shipping_address": client.address,
            "shipping_city": client.city,
            "shipping_state": client.state,
            "shipping_pin_code": client.pin_code,
        }

    def create(self, validated_data):
        items_data = validated_data.pop("items")

        delivery_challans = validated_data.pop(
            "delivery_challans",
            [],
        )

        request = self.context["request"]

        try:
            admin = request.user.admin_profile
        except AttributeError:
            raise serializers.ValidationError(
                {
                    "detail": (
                        "An active admin profile is required."
                    )
                }
            )

        if not admin.is_active:
            raise serializers.ValidationError(
                {
                    "detail": (
                        "An active admin profile is required."
                    )
                }
            )

        client = validated_data["client"]

        # Create historical billing snapshot.
        validated_data.update(
            self._client_billing_snapshot(client)
        )

        # Default shipping information from the client.
        shipping_defaults = self._default_shipping_snapshot(
            client
        )

        for field, value in shipping_defaults.items():
            validated_data.setdefault(field, value)

        additional_charges = validated_data.get(
            "additional_charges",
            Decimal("0.00"),
        )

        gst_type = validated_data.get("gst_type")

        prepared_items = []

        for item in items_data:
            paint = item["paint"]

            item["description"] = (
                item.get("description")
                or paint.name
            )

            item["hsn_sac_code"] = paint.hsn_sac_code
            item["gst_percentage"] = paint.gst_percentage

            _, taxable_amount, gst_amount = (
                self._calculate_item(item)
            )

            if gst_type == Invoice.GSTType.INTRA_STATE:
                item_gst = gst_amount

            elif gst_type == Invoice.GSTType.INTER_STATE:
                item_gst = gst_amount

            else:
                raise serializers.ValidationError(
                    {"gst_type": "GST type is required."}
                )

            item["line_total"] = (
                taxable_amount + item_gst
            ).quantize(Decimal("0.01"))

            prepared_items.append(item)

        totals = self._calculate_totals(
            prepared_items,
            gst_type,
            additional_charges,
        )

        validated_data.update(totals)
        validated_data["created_by"] = admin

        with transaction.atomic():
            invoice = Invoice.objects.create(
                **validated_data
            )

            InvoiceItem.objects.bulk_create(
                [
                    InvoiceItem(
                        invoice=invoice,
                        **item,
                    )
                    for item in prepared_items
                ]
            )

            if delivery_challans:
                invoice.delivery_challans.set(
                    delivery_challans
                )

        return invoice

    def update(self, instance, validated_data):
        items_data = validated_data.pop(
            "items",
            None,
        )

        delivery_challans = validated_data.pop(
            "delivery_challans",
            None,
        )

        gst_type = validated_data.get(
            "gst_type",
            instance.gst_type,
        )

        additional_charges = validated_data.get(
            "additional_charges",
            instance.additional_charges,
        )

        # If items were supplied, rebuild the invoice items
        # from the submitted data.
        if items_data is not None:
            prepared_items = []

            for item in items_data:
                paint = item["paint"]

                item["description"] = (
                    item.get("description")
                    or paint.name
                )

                item["hsn_sac_code"] = paint.hsn_sac_code
                item["gst_percentage"] = paint.gst_percentage

                _, taxable_amount, gst_amount = (
                    self._calculate_item(item)
                )

                item["line_total"] = (
                    taxable_amount + gst_amount
                ).quantize(Decimal("0.01"))

                prepared_items.append(item)

        # If items were not supplied, recalculate using
        # the existing invoice items.
        else:
            prepared_items = []

            for item in instance.items.all():
                item_data = {
                    "paint": item.paint,
                    "description": item.description,
                    "hsn_sac_code": item.hsn_sac_code,
                    "batch_number": item.batch_number,
                    "pack_description": item.pack_description,
                    "quantity": item.quantity,
                    "unit_price": item.unit_price,
                    "gst_percentage": item.gst_percentage,
                    "line_discount": item.line_discount,
                }

                _, taxable_amount, gst_amount = (
                    self._calculate_item(item_data)
                )

                item_data["line_total"] = (
                    taxable_amount + gst_amount
                ).quantize(Decimal("0.01"))

                prepared_items.append(item_data)

        totals = self._calculate_totals(
            prepared_items,
            gst_type,
            additional_charges,
        )

        validated_data.update(totals)

        with transaction.atomic():
            for field, value in validated_data.items():
                setattr(instance, field, value)

            instance.save()

            if items_data is not None:
                instance.items.all().delete()

                InvoiceItem.objects.bulk_create(
                    [
                        InvoiceItem(
                            invoice=instance,
                            **item,
                        )
                        for item in prepared_items
                    ]
                )

            if delivery_challans is not None:
                instance.delivery_challans.set(
                    delivery_challans
                )

        return instance