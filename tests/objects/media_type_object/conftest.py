import pytest


@pytest.fixture
def fx_media_type_object__required(fx_schema_object__required) -> dict:
    return {'schema': fx_schema_object__required}


@pytest.fixture
def fx_media_type_object__full(
    fx_media_type_object__required, fx_schema_object__full, fx_example_object_full
) -> dict:
    return {
        **fx_media_type_object__required,
        'schema': fx_schema_object__full,
        'itemSchema': fx_schema_object__full,
        'examples': {'example1': fx_example_object_full},
    }
