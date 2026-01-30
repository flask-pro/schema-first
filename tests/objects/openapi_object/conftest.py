import pytest


@pytest.fixture
def fx_openapi_object__required(fx_info_object_required, fx_paths_object_required) -> dict:
    return {'openapi': '3.2.0', 'info': fx_info_object_required, 'paths': fx_paths_object_required}


@pytest.fixture
def fx_openapi_object_full(
    fx_openapi_object__required,
    fx_info_object_full,
    fx_server_object_full,
    fx_paths_object_full,
    fx_external_docs_object_full,
    fx_tag_object_full,
):
    return {
        **fx_openapi_object__required,
        'info': fx_info_object_full,
        'jsonSchemaDialect': 'https://json-schema.org/draft/2020-12/schema',
        'servers': [fx_server_object_full],
        'paths': fx_paths_object_full,
        'tags': [fx_tag_object_full],
        'externalDocs': fx_external_docs_object_full,
    }
