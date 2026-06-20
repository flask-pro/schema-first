import pytest


@pytest.fixture
def fx_security_scheme_object_basic_required() -> dict:
    return {'type': 'http', 'scheme': 'Basic'}


@pytest.fixture
def fx_security_scheme_object_basic_full(fx_security_scheme_object_basic_required) -> dict:
    return {
        **fx_security_scheme_object_basic_required,
        'description': 'HTTP Basic authorization schema.',
        'deprecated': False,
    }


@pytest.fixture
def fx_security_scheme_object_bearer_required() -> dict:
    return {'type': 'http', 'scheme': 'Bearer', 'name': 'Authorization', 'in': 'header'}


@pytest.fixture
def fx_security_scheme_object_bearer_full(fx_security_scheme_object_bearer_required) -> dict:
    return {
        **fx_security_scheme_object_bearer_required,
        'bearerFormat': 'legalact',
        'description': 'Bearer authorization schema.',
        'deprecated': False,
    }
