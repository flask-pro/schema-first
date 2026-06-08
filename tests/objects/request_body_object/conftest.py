import pytest


@pytest.fixture
def fx_request_body_object_required(fx_media_type_object_required) -> dict:
    return {
        'content': {'application/json': fx_media_type_object_required},
    }


@pytest.fixture
def fx_request_body_object_full(fx_request_body_object_required, fx_media_type_object_full) -> dict:
    return {
        **fx_request_body_object_required,
        'description': 'Full Request Body Object.',
        'content': {'application/json': fx_media_type_object_full},
        'required': True,
    }
