import pytest


@pytest.fixture
def fx_field_boolean__required() -> dict:
    return {'type': 'boolean'}


@pytest.fixture
def fx_field_boolean__full(fx_field_boolean__required) -> dict:
    return {
        **fx_field_boolean__required,
        'nullable': True,
        'description': 'Example to boolean field.',
        'default': True,
    }
