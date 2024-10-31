"""Module containing urls for wallets."""

from django.urls import path

from src.wallets.views import WalletListCreateView

urlpatterns = [
    path("", WalletListCreateView.as_view()),
]
