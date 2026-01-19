import pytest


@pytest.fixture
def fx_external_docs_object_required() -> dict:
    return {'url': 'https://example.com'}


@pytest.fixture
def fx_external_docs_object_full(fx_external_docs_object_required) -> dict:
    return {
        **fx_external_docs_object_required,
        'description': 'Find more info here',
    }
