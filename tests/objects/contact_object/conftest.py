import pytest


@pytest.fixture
def fx_contact_object__required() -> dict:
    return {}


@pytest.fixture
def fx_contact_object__full(fx_contact_object__required) -> dict:
    return {
        **fx_contact_object__required,
        'name': 'API Support',
        'url': 'https://www.example.com/support',
        'email': 'support@example.com',
    }
