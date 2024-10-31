"""Module containing urls for transactions."""

from django.urls import path

from src.transactions.views import TransactionListCreateView

urlpatterns = [
    path("", TransactionListCreateView.as_view()),
]
