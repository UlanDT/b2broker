"""Module containing wallet model."""

from decimal import Decimal

from django.core.validators import MinValueValidator
from django.db import models
from django_stubs_ext.db.models import TypedModelMeta


class Wallet(models.Model):
    """Wallet model."""

    label = models.CharField(max_length=256)
    balance = models.DecimalField(
        max_digits=14, decimal_places=4, default=0.0000, validators=[MinValueValidator(Decimal("0.0000"))]
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    objects = models.Manager()

    class Meta(TypedModelMeta):
        """Meta class."""

        db_table = "wallets"
        ordering = ("-created_at",)

    def __str__(self) -> str:
        return self.label
