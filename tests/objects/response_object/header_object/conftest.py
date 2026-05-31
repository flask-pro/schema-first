import pytest


@pytest.fixture
def fx_header_object_full(fx_parameter_object_from_path_full) -> dict:
    header_object = {
        k: v for k, v in fx_parameter_object_from_path_full.items() if k not in ['name', 'in']
    }
    return header_object
