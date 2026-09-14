from django.core.validators import MaxValueValidator, MinValueValidator
from django.db import models


class Category(models.Model):
    name = models.CharField(max_length=100, unique=True)

    parent = models.ForeignKey(
        "self",
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="subcategories",
    )

    class Meta:
        db_table = "products_category"
        ordering = ["name"]

    def __str__(self):
        return self.name


class Paint(models.Model):
    class Finish(models.TextChoices):
        MATTE = "MATTE", "Matte"
        GLOSSY = "GLOSSY", "Glossy"
        SATIN = "SATIN", "Satin"
        EGGSHELL = "EGGSHELL", "Eggshell"
        SEMI_GLOSS = "SEMI_GLOSS", "Semi Gloss"

    name = models.CharField(
        max_length=150,
        db_index=True,
    )

    category = models.ForeignKey(
        Category,
        on_delete=models.PROTECT,
        related_name="paints",
    )

    finish = models.CharField(
        max_length=50,
        choices=Finish.choices,
    )

    color = models.CharField(max_length=50)

    shade_code = models.CharField(max_length=20)

    size = models.CharField(
        max_length=20,
        help_text="Example: 1L, 4L, 20L",
    )

    price = models.DecimalField(
        max_digits=10,
        decimal_places=2,
        validators=[
            MinValueValidator(0),
        ],
    )

    gst_percentage = models.DecimalField(
        max_digits=5,
        decimal_places=2,
        validators=[
            MinValueValidator(0),
            MaxValueValidator(100),
        ],
    )

    hsn_sac_code = models.CharField(
        max_length=20,
        blank=True,
        null=True,
    )

    description = models.TextField(
        blank=True,
        null=True,
    )

    is_available = models.BooleanField(default=True)

    created_at = models.DateTimeField(auto_now_add=True)

    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = "products_paint"

        indexes = [
            models.Index(fields=["category"]),
            models.Index(fields=["shade_code"]),
        ]

        constraints = [
            models.CheckConstraint(
                condition=models.Q(price__gte=0),
                name="paint_price_gte_zero",
            ),
            models.CheckConstraint(
                condition=models.Q(
                    gst_percentage__gte=0,
                    gst_percentage__lte=100,
                ),
                name="paint_gst_percentage_0_100",
            ),
        ]

    def __str__(self):
        return self.name


class PaintImage(models.Model):
    paint = models.ForeignKey(
        Paint,
        on_delete=models.CASCADE,
        related_name="images",
    )

    image = models.ImageField(
        upload_to="products/",
    )

    is_primary = models.BooleanField(
        default=False,
    )

    created_at = models.DateTimeField(
        auto_now_add=True,
    )

    class Meta:
        db_table = "products_paint_image"

    def __str__(self):
        return f"{self.paint.name} - Image"