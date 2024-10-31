"""Module containing views for wallets."""

from typing import Any

from rest_framework import filters, generics
from rest_framework.request import Request
from rest_framework.response import Response

from src.wallets.models import Wallet
from src.wallets.serializers import WalletCreateSerializer, WalletSerializer


class WalletListCreateView(generics.ListCreateAPIView):
    """API for fetching and creating wallets."""

    queryset = Wallet.objects.all()
    filter_backends = (filters.OrderingFilter, filters.SearchFilter)
    ordering_fields = ["label", "balance"]
    search_fields = ["label"]

    def post(self, request: Request, *args: Any, **kwargs: Any) -> Response:
        """Create new wallet."""
        return super().post(request, *args, **kwargs)

    def get(self, request: Request, *args: Any, **kwargs: Any) -> Response:
        """List wallets with basic pagination and filtering."""
        return super().list(request, *args, **kwargs)

    def get_serializer_class(self) -> type[WalletSerializer] | type[WalletCreateSerializer]:
        """Get serializer class."""
        if self.request.method == "GET":
            return WalletSerializer
        return WalletCreateSerializer
