"""Module containing project fixtures."""

import pytest
from rest_framework.test import APIClient


@pytest.fixture
def api_client() -> APIClient:
    """Test client."""
    return APIClient()
