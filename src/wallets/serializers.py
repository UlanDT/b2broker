"""Module containing serializers for wallets."""

from rest_framework import serializers

from src.wallets.models import Wallet


class WalletSerializer(serializers.ModelSerializer):
    """Serialize Wallet instance."""

    class Meta:
        """Meta class."""

        model = Wallet
        fields = (
            "id",
            "label",
            "balance",
        )


class WalletCreateSerializer(serializers.ModelSerializer):
    """Serialize Wallet instance for post request."""

    class Meta:
        """Meta class."""

        model = Wallet
        fields = (
            "id",
            "label",
        )
