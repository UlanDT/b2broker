"""Module containing views for transactions."""

import logging
from typing import Any

from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import generics
from rest_framework.filters import OrderingFilter
from rest_framework.request import Request
from rest_framework.response import Response

from .models import Transaction
from .serializers import TransactionCreateSerializer, TransactionSerializer
from .services.transaction_services import TransactionService

logger = logging.getLogger(__name__)


class TransactionListCreateView(generics.ListCreateAPIView):
    """API for fetching and creating transactions."""

    queryset = Transaction.objects.select_related("wallet")
    filter_backends = [DjangoFilterBackend, OrderingFilter]
    filterset_fields = ["wallet", "txid"]
    ordering_fields = ["amount", "created_at"]
    ordering = ["created_at"]

    service = TransactionService()

    def perform_create(self, serializer: TransactionCreateSerializer) -> None:
        """Handle wallet transaction."""
        # Wrap the operation in an atomic transaction
        wallet = serializer.validated_data["wallet"]
        amount = serializer.validated_data["amount"]
        self.service.create(wallet, amount)
        serializer.save()

    def post(self, request: Request, *args: Any, **kwargs: Any) -> Response:
        """Create new transaction."""
        logger.info(
            "Creating transaction. Amount: %s, Wallet: %s",
            request.data["amount"],
            request.data["wallet"],
        )
        return super().post(request, *args, **kwargs)

    def get(self, request: Request, *args: Any, **kwargs: Any) -> Response:
        """List transactions with basic pagination and filtering."""
        return super().list(request, *args, **kwargs)

    def get_serializer_class(self) -> type[TransactionSerializer] | type[TransactionCreateSerializer]:
        """Get serializer class."""
        if self.request.method == "GET":
            return TransactionSerializer
        return TransactionCreateSerializer
