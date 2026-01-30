import pytest


@pytest.fixture
def fx_responses_object__required(fx_response_object__required) -> dict:
    return {'200': fx_response_object__required}


@pytest.fixture
def fx_responses_object__full(fx_responses_object__required, fx_response_object__full) -> dict:
    return {
        **fx_responses_object__required,
        '200': fx_response_object__full,
        'default': fx_response_object__full,
    }
