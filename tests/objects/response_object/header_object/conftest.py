import pytest


@pytest.fixture
def fx_header_object_full(fx_parameter_object_from_path_full) -> dict:
    fx_parameter_object_from_path_full.pop('name')
    fx_parameter_object_from_path_full.pop('in')
    return fx_parameter_object_from_path_full
