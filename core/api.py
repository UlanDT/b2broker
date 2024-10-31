"""API urls."""

from django.urls import include, path

urlpatterns = [
    path("wallets/", include("src.wallets.urls")),
    path("transactions/", include("src.transactions.urls")),
]
