"""Module containing transaction model."""

import uuid

from django.db import models
from django_stubs_ext.db.models import TypedModelMeta

from src.wallets.models import Wallet


class Transaction(models.Model):
    """Transaction model."""

    wallet = models.ForeignKey(Wallet, on_delete=models.PROTECT)

    # Transaction id should not be editable and be generated in backend only.
    txid = models.UUIDField(
        default=uuid.uuid4,
        unique=True,
        db_index=True,
        editable=False,
    )
    amount = models.DecimalField(max_digits=14, decimal_places=4, default=0.00)
    created_at = models.DateTimeField(auto_now_add=True)

    objects = models.Manager()

    class Meta(TypedModelMeta):
        """Meta class."""

        db_table = "transactions"

    def __str__(self) -> str:
        return str(self.txid)
