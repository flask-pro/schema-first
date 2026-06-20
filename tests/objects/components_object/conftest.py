import pytest


@pytest.fixture
def fx_components_object_full(
    fx_schema_object_full,
    fx_response_object_full,
    fx_parameter_object_from_path_full,
    fx_example_object_full,
    fx_request_body_object_full,
    fx_header_object_full,
    fx_security_scheme_object_basic_full,
    fx_security_scheme_object_bearer_full,
    fx_path_item_object_full,
    fx_media_type_object_full,
):
    return {
        'schemas': {'schema_to_components': fx_schema_object_full},
        'responses': {'responses_to_components': fx_response_object_full},
        'parameters': {'parameters_to_components': fx_parameter_object_from_path_full},
        'examples': {'examples_to_components': fx_example_object_full},
        'requestBodies': {'requestBodies_to_components': fx_request_body_object_full},
        'headers': {'headers_to_components': fx_header_object_full},
        'securitySchemes': {
            'BasicAuth': fx_security_scheme_object_basic_full,
            'BearerAuth': fx_security_scheme_object_bearer_full,
        },
        'pathItems': {'pathItems_to_components': fx_path_item_object_full},
        'mediaTypes': {'mediaTypes_to_components': fx_media_type_object_full},
    }
