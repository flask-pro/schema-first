import pytest


@pytest.fixture
def fx_contact_object_required() -> dict:
    return {}


@pytest.fixture
def fx_contact_object_full(fx_contact_object_required) -> dict:
    return {
        **fx_contact_object_required,
        'name': 'API Support',
        'url': 'https://www.example.com/support',
        'email': 'support@example.com',
    }
