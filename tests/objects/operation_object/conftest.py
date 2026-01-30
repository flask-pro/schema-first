import pytest


@pytest.fixture
def fx_operation_object_required(fx_responses_object_required) -> dict:
    return {'responses': fx_responses_object_required}


@pytest.fixture
def fx_operation_object_full(
    fx_operation_object_required,
    fx_external_docs_object_full,
    fx_responses_object_full,
    fx_server_object_full,
) -> dict:
    return {
        **fx_operation_object_required,
        'tags': ['test_endpoint'],
        'summary': 'Full operation object.',
        'description': 'Full operation object from fixture.',
        'externalDocs': fx_external_docs_object_full,
        'operationId': 'endpoint-get',
        'responses': fx_responses_object_full,
        'deprecated': False,
        'servers': [fx_server_object_full],
    }
