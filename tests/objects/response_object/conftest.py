import pytest


@pytest.fixture
def fx_response_object_required(fx_media_type_object_required) -> dict:
    return {
        'description': 'OK',
        'content': {'application/json': fx_media_type_object_required},
    }


@pytest.fixture
def fx_response_object_full(fx_response_object_required, fx_media_type_object_full) -> dict:
    return {
        **fx_response_object_required,
        'summary': 'Full Response Object.',
        'content': {'application/json': fx_media_type_object_full},
    }
