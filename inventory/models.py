from django.core.validators import MinValueValidator
from django.db import models

from products.models import Paint


class Stock(models.Model):
    paint = models.OneToOneField(
        Paint,
        on_delete=models.CASCADE,
        related_name="stock",
    )
    quantity = models.IntegerField(
        default=0,
        validators=[MinValueValidator(0)],
    )
    low_stock_threshold = models.IntegerField(
        default=10,
        validators=[MinValueValidator(0)],
    )
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = "inventory_stock"
        constraints = [
            models.CheckConstraint(
                condition=models.Q(quantity__gte=0),
                name="stock_quantity_gte_zero",
            ),
            models.CheckConstraint(
                condition=models.Q(low_stock_threshold__gte=0),
                name="stock_threshold_gte_zero",
            ),
        ]

    def __str__(self):
        return f"{self.paint.name} - {self.quantity}"


class StockMovement(models.Model):
    class MovementType(models.TextChoices):
        IN = "IN", "Stock In"
        OUT = "OUT", "Stock Out"
        ADJUSTMENT = "ADJUSTMENT", "Adjustment"

    paint = models.ForeignKey(
        Paint,
        on_delete=models.PROTECT,
        related_name="stock_movements",
    )
    movement_type = models.CharField(
        max_length=20,
        choices=MovementType.choices,
    )
    quantity = models.IntegerField(
        validators=[MinValueValidator(1)],
    )
    reference_invoice = models.ForeignKey(
        "invoices.Invoice",
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="stock_movements",
    )
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = "inventory_stock_movement"
        indexes = [
            models.Index(fields=["paint"]),
            models.Index(fields=["movement_type"]),
            models.Index(fields=["reference_invoice"]),
        ]
        constraints = [
            models.CheckConstraint(
                condition=models.Q(quantity__gt=0),
                name="stock_movement_quantity_gt_zero",
            ),
        ]

    def __str__(self):
        return f"{self.paint.name} - {self.movement_type}"