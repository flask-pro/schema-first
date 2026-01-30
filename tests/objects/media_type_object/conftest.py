import pytest


@pytest.fixture
def fx_media_type_object_required(fx_schema_object_required) -> dict:
    return {'schema': fx_schema_object_required}


@pytest.fixture
def fx_media_type_object_full(
    fx_media_type_object_required, fx_schema_object_full, fx_example_object_full
) -> dict:
    return {
        **fx_media_type_object_required,
        'schema': fx_schema_object_full,
        'itemSchema': fx_schema_object_full,
        'examples': {'example1': fx_example_object_full},
    }
