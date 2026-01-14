import pytest


@pytest.fixture
def fx_field_number__required() -> dict:
    return {'type': 'number'}


@pytest.fixture
def fx_field_number__full(fx_field_number__required) -> dict:
    return {
        **fx_field_number__required,
        'nullable': True,
        'description': 'Example to number field.',
        'minimum': -10.0,
        'maximum': 10,
        'exclusiveMinimum': -5.0,
        'exclusiveMaximum': 5,
        'multipleOf': 0.5,
        'default': 0.0,
    }
