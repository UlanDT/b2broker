"""Module containing tests for transactions api."""

import uuid
from decimal import Decimal
from itertools import cycle

import pytest
from rest_framework.test import APIClient

from src.transactions.models import Transaction
from src.wallets.models import Wallet
from tests import recipe


@pytest.mark.django_db
def test_success_create_transaction(api_client: APIClient) -> None:
    """Test success create transaction."""
    # Given: a wallet to create transactions to and a request body
    recipe.wallet.make(label="test", balance=0)

    data = {"wallet": "1", "amount": "500"}

    # When: a POST request is sent
    response = api_client.post(path="/api/transactions/", data=data)

    # Then: the transaction is created and a 201 status code is returned
    assert response.status_code == 201

    tx = Transaction.objects.first()
    assert tx is not None
    assert tx.amount == Decimal("500.0000")

    wallet = Wallet.objects.first()
    assert wallet is not None
    assert wallet.balance == Decimal("500.0000")


@pytest.mark.django_db
def test_success_create_negative_transaction(api_client: APIClient) -> None:
    """Test success create negative transaction."""
    # Given: a wallet to create transactions to and a request body
    recipe.wallet.make(label="test", balance=500)

    data = {"wallet": "1", "amount": "-200"}

    # When: a POST request is sent
    response = api_client.post(path="/api/transactions/", data=data)

    # Then: the transaction is created and a 201 status code is returned
    assert response.status_code == 201

    tx = Transaction.objects.first()
    assert tx is not None
    assert tx.amount == Decimal("-200.0000")

    wallet = Wallet.objects.first()
    assert wallet is not None
    assert wallet.balance == Decimal("300.0000")


@pytest.mark.django_db
def test_fail_create_negative_transaction_not_enough_balance(api_client: APIClient) -> None:
    """Test fail to create transaction due to insufficient balance."""
    # Given: a wallet to create transactions to and a request body
    recipe.wallet.make(label="test", balance=500)

    data = {"wallet": "1", "amount": "-700"}

    # When: a POST request is sent
    response = api_client.post(path="/api/transactions/", data=data)

    # Then: the transaction is not craeted and 400 status code is returned
    assert response.status_code == 400
    assert Transaction.objects.count() == 0

    wallet = Wallet.objects.first()
    assert wallet is not None
    assert wallet.balance == Decimal("500.0000")


@pytest.mark.django_db
def test_fail_create_transaction_wallet_not_found(api_client: APIClient) -> None:
    """Test fail to create transaction due to missing wallet."""
    # Given: a request body
    data = {"wallet": "1", "amount": "700"}

    # When: a POST request is sent
    response = api_client.post(path="/api/transactions/", data=data)

    # Then: the transaction is not craeted and 400 status code is returned
    assert response.status_code == 400
    assert Transaction.objects.count() == 0


@pytest.mark.django_db
def test_fetch_transactions_with_wallet_filters(api_client: APIClient) -> None:
    """Test fetch transactions with wallet query param."""
    # Given: wallets to create transactions to and a request body
    requested_wallet = recipe.wallet.make()
    wallet = recipe.wallet.make()
    recipe.transaction.make(wallet=requested_wallet, amount=500)
    recipe.transaction.make(wallet=wallet, amount=300)

    data = {"wallet": "1"}

    # When: a GET request is sent with wallet query params
    response = api_client.get(path="/api/transactions/", data=data)

    # Then: we check that the response contains transactions only for requested wallet
    assert response.status_code == 200
    assert response.data["count"] == 1
    assert response.data["results"][0]["wallet"]["id"] == requested_wallet.pk


@pytest.mark.django_db
def test_fetch_transactions_with_txid_filters(api_client: APIClient) -> None:
    """Test fetch transactions with txid query param."""
    # Given: wallets to create transactions to and a request body
    requested_uuid = uuid.uuid4()
    wallet = recipe.wallet.make()
    recipe.transaction.make(
        _quantity=5,
        wallet=wallet,
        txid=cycle((requested_uuid, uuid.uuid4(), uuid.uuid4(), uuid.uuid4(), uuid.uuid4())),
        amount=300,
    )

    data = {"txid": str(requested_uuid)}

    # When: a GET request is sent with txid query params
    response = api_client.get(path="/api/transactions/", data=data)

    # Then: we check that the response contains transactions only for requested txid
    assert response.status_code == 200
    assert response.data["count"] == 1
    assert response.data["results"][0]["txid"] == str(requested_uuid)
