"""Module containing admin configs for transactions."""

from django.contrib import admin

from src.transactions.models import Transaction


@admin.register(Transaction)
class TransactionAdmin(admin.ModelAdmin[Transaction]):
    """Custom admin for transaction."""

    list_display = (
        "wallet",
        "txid",
        "amount",
    )
