"""Module containing command to generate wallets."""

import logging
from argparse import ArgumentParser
from typing import Any

from django.core.management import BaseCommand
from faker import Faker

from src.wallets.models import Wallet

logger = logging.getLogger(__name__)
DEFAULT_AMOUNT = 10
fake = Faker()


class Command(BaseCommand):
    """Management command to generate wallets."""

    def add_arguments(self, parser: ArgumentParser) -> None:
        """Parse command arguments."""
        parser.add_argument("--amount")

    def handle(self, *args: Any, **options: Any) -> None:
        """Entrypoint function."""
        amount = self.get_amount(options.get("amount", DEFAULT_AMOUNT))
        logger.info("Creating %s wallets", amount)

        self.create_wallets(amount)
        logger.info("Successfully created %s wallets", amount)

    def get_amount(self, amount: str | int) -> int:
        """Get amount of wallets to create."""
        if not amount:
            return DEFAULT_AMOUNT

        try:
            return int(amount)
        except ValueError:
            msg = "Provided amount of %s is not an integer. Creating default amount of wallets."
            logger.warning(msg, amount)
            return DEFAULT_AMOUNT

    def create_wallets(self, amount: int) -> None:
        """Create wallets.

        Used phone number as a lable just for example
        """
        wallets = [
            Wallet(
                label=fake.phone_number(),
                balance=fake.pydecimal(left_digits=10, right_digits=4, min_value=0.01),
            )
            for _ in range(amount)
        ]

        Wallet.objects.bulk_create(wallets)
