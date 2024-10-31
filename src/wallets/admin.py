"""Module containing admin configs for wallets."""

from django.contrib import admin

from src.transactions.models import Transaction
from src.wallets.models import Wallet


class TransactionInline(admin.TabularInline):  # type: ignore
    """Transaction inline."""

    model = Transaction
    extra = 1
    fields = ("id", "txid", "amount", "created_at")


@admin.register(Wallet)
class WalletAdmin(admin.ModelAdmin[Wallet]):
    """Custom admin for wallet."""

    list_display = (
        "label",
        "balance",
    )
    inlines = [TransactionInline]
