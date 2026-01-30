import pytest


@pytest.fixture
def fx_response_object__required(fx_media_type_object__required) -> dict:
    return {
        'description': 'OK',
        'content': {'application/json': fx_media_type_object__required},
    }


@pytest.fixture
def fx_response_object__full(fx_response_object__required, fx_media_type_object__full) -> dict:
    return {
        **fx_response_object__required,
        'summary': 'Full Response Object.',
        'content': {'application/json': fx_media_type_object__full},
    }
