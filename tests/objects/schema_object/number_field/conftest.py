import pytest


@pytest.fixture
def fx_field_number_required() -> dict:
    return {'type': 'number'}


@pytest.fixture
def fx_field_number_full(fx_field_number_required) -> dict:
    return {
        **fx_field_number_required,
        'nullable': True,
        'description': 'Example to number field.',
        'minimum': -10.0,
        'maximum': 10,
        'exclusiveMinimum': -5.0,
        'exclusiveMaximum': 5,
        'multipleOf': 0.5,
        'default': 0.1,
    }


@pytest.fixture
def fx_field_number__float(fx_field_number_full) -> dict:
    return {**fx_field_number_full, 'format': 'float'}


@pytest.fixture
def fx_field_number__double(fx_field_number_full) -> dict:
    return {**fx_field_number_full, 'format': 'double'}
