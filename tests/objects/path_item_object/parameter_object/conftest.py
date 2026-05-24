import pytest


@pytest.fixture
def fx_parameter_object_required() -> dict:
    return {'name': 'id', 'in': 'path'}


@pytest.fixture
def fx_parameter_object_full(fx_parameter_object_required, fx_example_object_full) -> dict:
    return {
        **fx_parameter_object_required,
        'description': 'Item ID',
        'required': False,
        'deprecated': True,
        'examples': {'ID': fx_example_object_full},
    }
