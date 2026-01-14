import pytest


@pytest.fixture
def fx_field_integer__required() -> dict:
    return {'type': 'integer'}


@pytest.fixture
def fx_field_integer__full(fx_field_integer__required) -> dict:
    return {
        **fx_field_integer__required,
        'nullable': True,
        'description': 'Example to integer field.',
        'minimum': -10,
        'maximum': 10,
        'exclusiveMinimum': -5,
        'exclusiveMaximum': 5,
        'multipleOf': 1,
        'default': 0,
    }
