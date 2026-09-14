from django.core.validators import MaxValueValidator, MinValueValidator
from django.db import models
from django.utils import timezone

from accounts.models import Admin
from clients.models import Client
from products.models import Paint


class Invoice(models.Model):
    class PaymentStatus(models.TextChoices):
        PAID = "PAID", "Paid"
        UNPAID = "UNPAID", "Unpaid"
        PARTIAL = "PARTIAL", "Partial"

    class PaymentMethod(models.TextChoices):
        CASH = "CASH", "Cash"
        UPI = "UPI", "UPI"
        CARD = "CARD", "Card"
        BANK_TRANSFER = "BANK_TRANSFER", "Bank Transfer"
        CHEQUE = "CHEQUE", "Cheque"

    class GSTType(models.TextChoices):
        INTRA_STATE = "INTRA_STATE", "Intra-State"
        INTER_STATE = "INTER_STATE", "Inter-State"

    invoice_number = models.CharField(
        max_length=30,
        unique=True,
    )
    client = models.ForeignKey(
        Client,
        on_delete=models.PROTECT,
        related_name="invoices",
    )
    delivery_challans = models.ManyToManyField(
        "DeliveryChallan",
        blank=True,
        related_name="invoices",
    )
    created_by = models.ForeignKey(
        Admin,
        on_delete=models.PROTECT,
        related_name="created_invoices",
    )
    invoice_date = models.DateField(
        default=timezone.localdate,
    )

    # Invoice document details
    po_number = models.CharField(
        max_length=50,
        blank=True,
        null=True,
    )
    payment_terms = models.CharField(
        max_length=100,
        blank=True,
        null=True,
    )
    classification = models.CharField(
        max_length=100,
        blank=True,
        null=True,
    )
    eway_bill_number = models.CharField(
        max_length=50,
        blank=True,
        null=True,
    )
    removal_date = models.DateField(
        blank=True,
        null=True,
    )
    removal_time = models.TimeField(
        blank=True,
        null=True,
    )
    dispatched_through = models.CharField(
        max_length=100,
        blank=True,
        null=True,
    )
    vehicle_number = models.CharField(
        max_length=30,
        blank=True,
        null=True,
    )
    lr_number = models.CharField(
        max_length=50,
        blank=True,
        null=True,
    )
    lr_date = models.DateField(
        blank=True,
        null=True,
    )

    # Billing address snapshot
    billing_name = models.CharField(
        max_length=150,
        blank=True,
        null=True,
    )
    billing_phone = models.CharField(
        max_length=15,
        blank=True,
        null=True,
    )
    billing_email = models.EmailField(
        max_length=254,
        blank=True,
        null=True,
    )
    billing_address = models.CharField(
        max_length=255,
        blank=True,
        null=True,
    )
    billing_city = models.CharField(
        max_length=100,
        blank=True,
        null=True,
    )
    billing_state = models.CharField(
        max_length=100,
        blank=True,
        null=True,
    )
    billing_pin_code = models.CharField(
        max_length=10,
        blank=True,
        null=True,
    )
    billing_gst_number = models.CharField(
        max_length=15,
        blank=True,
        null=True,
    )

    # Shipping snapshot
    shipping_name = models.CharField(
        max_length=150,
        blank=True,
        null=True,
    )
    shipping_address = models.CharField(
        max_length=255,
        blank=True,
        null=True,
    )
    shipping_city = models.CharField(
        max_length=100,
        blank=True,
        null=True,
    )
    shipping_state = models.CharField(
        max_length=100,
        blank=True,
        null=True,
    )
    shipping_pin_code = models.CharField(
        max_length=10,
        blank=True,
        null=True,
    )

    # GST and totals
    gst_type = models.CharField(
        max_length=20,
        choices=GSTType.choices,
        blank=True,
        null=True,
    )
    subtotal = models.DecimalField(
        max_digits=12,
        decimal_places=2,
        validators=[MinValueValidator(0)],
    )
    discount_amount = models.DecimalField(
        max_digits=12,
        decimal_places=2,
        default=0,
        validators=[MinValueValidator(0)],
    )
    taxable_amount = models.DecimalField(
        max_digits=12,
        decimal_places=2,
        blank=True,
        null=True,
        validators=[MinValueValidator(0)],
    )
    cgst_amount = models.DecimalField(
        max_digits=12,
        decimal_places=2,
        default=0,
        validators=[MinValueValidator(0)],
    )
    sgst_amount = models.DecimalField(
        max_digits=12,
        decimal_places=2,
        default=0,
        validators=[MinValueValidator(0)],
    )
    igst_amount = models.DecimalField(
        max_digits=12,
        decimal_places=2,
        default=0,
        validators=[MinValueValidator(0)],
    )
    gst_amount = models.DecimalField(
        max_digits=12,
        decimal_places=2,
        validators=[MinValueValidator(0)],
    )
    additional_charges = models.DecimalField(
        max_digits=12,
        decimal_places=2,
        default=0,
        validators=[MinValueValidator(0)],
    )
    round_off = models.DecimalField(
        max_digits=12,
        decimal_places=2,
        default=0,
    )
    grand_total = models.DecimalField(
        max_digits=12,
        decimal_places=2,
        validators=[MinValueValidator(0)],
    )

    # Payment details
    payment_status = models.CharField(
        max_length=20,
        choices=PaymentStatus.choices,
        default=PaymentStatus.UNPAID,
    )
    payment_method = models.CharField(
        max_length=30,
        choices=PaymentMethod.choices,
        blank=True,
        null=True,
    )

    notes = models.TextField(
        blank=True,
        null=True,
    )
    pdf_file = models.FileField(
        upload_to="invoices/",
        blank=True,
        null=True,
    )
    created_at = models.DateTimeField(
        auto_now_add=True,
    )
    updated_at = models.DateTimeField(
        auto_now=True,
    )

    class Meta:
        db_table = "invoices_invoice"
        indexes = [
            models.Index(fields=["invoice_date"]),
            models.Index(fields=["payment_status"]),
            models.Index(fields=["client", "invoice_date"]),
        ]

    def __str__(self):
        return self.invoice_number


class InvoiceItem(models.Model):
    invoice = models.ForeignKey(
        Invoice,
        on_delete=models.CASCADE,
        related_name="items",
    )
    paint = models.ForeignKey(
        Paint,
        on_delete=models.PROTECT,
        related_name="invoice_items",
    )

    # Invoice snapshot fields
    description = models.CharField(
        max_length=150,
        blank=True,
        null=True,
    )
    hsn_sac_code = models.CharField(
        max_length=20,
        blank=True,
        null=True,
    )
    batch_number = models.CharField(
        max_length=50,
        blank=True,
        null=True,
    )
    pack_description = models.CharField(
        max_length=50,
        blank=True,
        null=True,
    )

    quantity = models.PositiveIntegerField(
        validators=[MinValueValidator(1)],
    )
    unit_price = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        validators=[MinValueValidator(0)],
    )
    gst_percentage = models.DecimalField(
        max_digits=5,
        decimal_places=2,
        validators=[
            MinValueValidator(0),
            MaxValueValidator(100),
        ],
    )
    line_discount = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        default=0,
        validators=[MinValueValidator(0)],
    )
    line_total = models.DecimalField(
        max_digits=12,
        decimal_places=2,
        validators=[MinValueValidator(0)],
    )

    class Meta:
        db_table = "invoices_invoice_item"
        indexes = [
            models.Index(fields=["invoice"]),
            models.Index(fields=["paint"]),
        ]

    def __str__(self):
        return f"{self.invoice.invoice_number} - {self.description or self.paint.name}"

class DeliveryChallan(models.Model):
    challan_number = models.CharField(
        max_length=50,
        unique=True,
    )
    challan_date = models.DateField(
        default=timezone.localdate,
    )

    client = models.ForeignKey(
        Client,
        on_delete=models.PROTECT,
        related_name="delivery_challans",
    )
    created_by = models.ForeignKey(
        Admin,
        on_delete=models.PROTECT,
        related_name="created_delivery_challans",
    )

    # Order / reference details
    po_number = models.CharField(
        max_length=50,
        blank=True,
        null=True,
    )
    classification = models.CharField(
        max_length=100,
        blank=True,
        null=True,
    )

    # Shipping snapshot
    shipping_name = models.CharField(
        max_length=150,
        blank=True,
        null=True,
    )
    shipping_address = models.CharField(
        max_length=255,
        blank=True,
        null=True,
    )
    shipping_city = models.CharField(
        max_length=100,
        blank=True,
        null=True,
    )
    shipping_state = models.CharField(
        max_length=100,
        blank=True,
        null=True,
    )
    shipping_pin_code = models.CharField(
        max_length=10,
        blank=True,
        null=True,
    )
    shipping_gst_number = models.CharField(
        max_length=15,
        blank=True,
        null=True,
    )

    # Dispatch details
    eway_bill_number = models.CharField(
        max_length=50,
        blank=True,
        null=True,
    )
    removal_date = models.DateField(
        blank=True,
        null=True,
    )
    removal_time = models.TimeField(
        blank=True,
        null=True,
    )
    dispatched_through = models.CharField(
        max_length=100,
        blank=True,
        null=True,
    )
    vehicle_number = models.CharField(
        max_length=30,
        blank=True,
        null=True,
    )
    lr_number = models.CharField(
        max_length=50,
        blank=True,
        null=True,
    )
    lr_date = models.DateField(
        blank=True,
        null=True,
    )

    notes = models.TextField(
        blank=True,
        null=True,
    )

    created_at = models.DateTimeField(
        auto_now_add=True,
    )
    updated_at = models.DateTimeField(
        auto_now=True,
    )

    class Meta:
        db_table = "invoices_delivery_challan"
        indexes = [
            models.Index(fields=["challan_date"]),
            models.Index(fields=["client", "challan_date"]),
        ]

    def __str__(self):
        return self.challan_number


class DeliveryChallanItem(models.Model):
    delivery_challan = models.ForeignKey(
        DeliveryChallan,
        on_delete=models.CASCADE,
        related_name="items",
    )
    paint = models.ForeignKey(
        Paint,
        on_delete=models.PROTECT,
        related_name="delivery_challan_items",
    )

    # Challan snapshot fields
    description = models.CharField(
        max_length=150,
        blank=True,
        null=True,
    )
    hsn_sac_code = models.CharField(
        max_length=20,
        blank=True,
        null=True,
    )
    batch_number = models.CharField(
        max_length=50,
        blank=True,
        null=True,
    )
    pack_description = models.CharField(
        max_length=50,
        blank=True,
        null=True,
    )

    quantity = models.PositiveIntegerField(
        validators=[MinValueValidator(1)],
    )

    created_at = models.DateTimeField(
        auto_now_add=True,
    )

    class Meta:
        db_table = "invoices_delivery_challan_item"
        indexes = [
            models.Index(fields=["delivery_challan"]),
            models.Index(fields=["paint"]),
        ]

    def __str__(self):
        return (
            f"{self.delivery_challan.challan_number} - "
            f"{self.description or self.paint.name}"
        )