"""Module containing tests for wallets api."""

from decimal import Decimal
from itertools import cycle

import pytest
from rest_framework.test import APIClient

from src.wallets.models import Wallet
from tests import recipe


@pytest.mark.django_db
def test_success_create_wallet(api_client: APIClient) -> None:
    """Test success create wallet."""
    # Given: a request body
    data = {"label": "test"}

    # When: a POST request is sent
    response = api_client.post(path="/api/wallets/", data=data)

    # Then: the wallet is created and a 201 status code is returned
    assert response.status_code == 201
    assert Wallet.objects.get(label="test") is not None


@pytest.mark.django_db
def test_create_wallet_ignores_amount(api_client: APIClient) -> None:
    """Test shouldn't create wallet with requested amount."""
    # Given: a request body
    data = {"label": "test", "amount": "-1000"}

    # When: a POST request is sent
    response = api_client.post(path="/api/wallets/", data=data)

    # Then: the wallet is created and its balance is 0
    assert response.status_code == 201
    assert Wallet.objects.get(label="test").balance == Decimal("0.0000")


@pytest.mark.django_db
def test_list_wallets_api_ordering_param(api_client: APIClient) -> None:
    """Test fetch wallets with ordering param."""
    # Given: a batch of wallets
    recipe.wallet.make(_quantity=10, balance=cycle((100, 200, -300, 500, 400, 1200, -800, 1000, -700, 900)))

    # When: a GET request is sent with ordering query params
    params = {
        "ordering": "balance",
    }
    response = api_client.get(path="/api/wallets/", data=params)

    # Then: we check that request is successfult and there are 10 wallets
    assert response.status_code == 200
    assert response.data["count"] == 10

    # Then: we check that request data is ordered by balance
    assert response.data["results"][0]["balance"] == "-800.0000"
    assert response.data["results"][-1]["balance"] == "1200.0000"


@pytest.mark.django_db
def test_list_wallets_api_pagination_param(api_client: APIClient) -> None:
    """Test fetch wallets with page param."""
    # Given: a batch of wallets
    recipe.wallet.make(_quantity=10, balance=cycle((100, 200, -300, 500, 400, 1200, -800, 1000, -700, 900)))

    # When: a GET request is sent with page query params
    params = {
        "page": "2",
    }
    response = api_client.get(path="/api/wallets/", data=params)

    # Then: we check that request returns 404
    assert response.status_code == 404

    # When: we create 11th wallet and make a second request
    recipe.wallet.make(balance=8000)
    response = api_client.get(path="/api/wallets/", data=params)

    # Then: we get first wallet due to ordering
    assert response.status_code == 200
    assert response.data["results"][0]["id"] == 1


@pytest.mark.django_db
def test_list_wallets_api_search_param(api_client: APIClient) -> None:
    """Test fetch wallets with search param."""
    # Given: a batch of wallets
    recipe.wallet.make(_quantity=2, label=cycle(("test1", "test2")))

    # When: a GET request is sent with search query params
    params = {
        "search": "1",
    }
    response = api_client.get(path="/api/wallets/", data=params)

    # Then: we check that request is successful and only 1 result is returned
    assert response.status_code == 200
    assert response.data["results"][0]["label"] == "test1"
