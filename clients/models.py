from django.core.validators import RegexValidator
from django.db import models


class Client(models.Model):
    phone_validator = RegexValidator(
        regex=r"^\d{10}$",
        message="Phone number must contain exactly 10 digits.",
    )

    name = models.CharField(
        max_length=150,
        db_index=True,
    )
    phone_number = models.CharField(
        max_length=15,
        unique=True,
        validators=[phone_validator],
    )
    email = models.EmailField(
        max_length=254,
        blank=True,
        null=True,
    )
    address = models.CharField(
        max_length=255,
        blank=True,
        null=True,
    )
    city = models.CharField(
        max_length=100,
        blank=True,
        null=True,
    )
    state = models.CharField(
        max_length=100,
        blank=True,
        null=True,
    )
    pin_code = models.CharField(
        max_length=10,
        blank=True,
        null=True,
    )
    gst_number = models.CharField(
        max_length=15,
        blank=True,
        null=True,
        unique=True,
    )
    registration_date = models.DateField(
        auto_now_add=True,
    )
    created_at = models.DateTimeField(
        auto_now_add=True,
    )
    updated_at = models.DateTimeField(
        auto_now=True,
    )

    class Meta:
        db_table = "clients_client"
        indexes = [
            models.Index(fields=["phone_number"]),
            models.Index(fields=["gst_number"]),
            models.Index(fields=["name"]),
        ]

    def __str__(self):
        return self.name