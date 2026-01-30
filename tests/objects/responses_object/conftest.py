import pytest


@pytest.fixture
def fx_responses_object_required(fx_response_object_required) -> dict:
    return {'200': fx_response_object_required}


@pytest.fixture
def fx_responses_object_full(fx_responses_object_required, fx_response_object_full) -> dict:
    return {
        **fx_responses_object_required,
        '200': fx_response_object_full,
        'default': fx_response_object_full,
    }
