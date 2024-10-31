"""Module containing serializers for transactions."""

from decimal import Decimal
from typing import TypedDict

from rest_framework import serializers

from ..wallets.models import Wallet
from ..wallets.serializers import WalletSerializer
from .models import Transaction


class TransactionCreateDict(TypedDict):
    """Annotate TransactionCreateSerializer data."""

    wallet: Wallet
    amount: Decimal


class TransactionCreateSerializer(serializers.ModelSerializer):
    """Serialize transaction instances for POST method."""

    class Meta:
        """Meta class."""

        model = Transaction
        fields = ("id", "wallet", "amount")
        extra_kwargs = {
            "amount": {"required": True},
        }

    def validate(self, data: TransactionCreateDict) -> TransactionCreateDict:
        """Ensure wallet has enough balance for the transaction amount."""
        wallet = data["wallet"]
        amount = data["amount"]

        if wallet.balance + amount < 0:
            raise serializers.ValidationError("Insufficient wallet balance for this transaction.")

        return data


class TransactionSerializer(serializers.ModelSerializer):
    """Serialize transaction instances."""

    wallet = WalletSerializer(read_only=True)

    class Meta:
        """Meta class."""

        model = Transaction
        fields = ("id", "wallet", "txid", "amount")
