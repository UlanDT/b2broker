"""Module containing recipes for tests."""

import random

from model_bakery.recipe import Recipe, seq  # type: ignore

from src.transactions.models import Transaction
from src.wallets.models import Wallet

wallet = Recipe(
    Wallet,
    label="+996500500500",
    balance=seq(random.randint(10000, 99999)),  # type: ignore
)


transaction = Recipe(
    Transaction,
    txid=seq(random.randint(1000000, 9999999)),  # type: ignore
    amount=seq(random.randint(-1000000, 9999999)),  # type: ignore
)
