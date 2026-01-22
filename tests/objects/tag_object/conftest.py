import pytest


@pytest.fixture
def fx_tag_object_required() -> dict:
    return {'name': 'test_endpoint'}


@pytest.fixture
def fx_tag_object_full(fx_tag_object_required, fx_external_docs_object_full) -> dict:
    return {
        **fx_tag_object_required,
        'summary': 'Partner',
        'description': 'Operations available to the partners network',
        'parent': 'test_endpoint',
        'kind': 'audience',
        'externalDocs': fx_external_docs_object_full,
    }
