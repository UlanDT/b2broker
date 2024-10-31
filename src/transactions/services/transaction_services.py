"""Module containing services for transactions."""

from decimal import Decimal

from django.db import transaction as db_transaction

from src.wallets.models import Wallet


class TransactionService:
    """Service class for transactions."""

    def create(self, wallet: Wallet, amount: Decimal) -> None:
        """Create transaction"""
        with db_transaction.atomic():
            wallet = Wallet.objects.select_for_update().get(id=wallet.pk)
            wallet.balance += amount
            wallet.save()
