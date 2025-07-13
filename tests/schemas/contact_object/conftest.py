import pytest


@pytest.fixture
def fx_contact_object_minimal() -> dict:
    return {}


@pytest.fixture
def fx_contact_object_full(fx_contact_object_minimal) -> dict:
    return {
        **fx_contact_object_minimal,
        'name': 'API Support',
        'url': 'https://www.example.com/support',
        'email': 'support@example.com',
    }
