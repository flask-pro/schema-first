from schema_first.query.validator import HTTPQueryValidator


def test_query_validators__request(fx_openapi_3_2_0, fx_open_spec):
    file_path = fx_openapi_3_2_0('query_validator.openapi.yaml')
    spec = fx_open_spec(file_path)
    query_validator = HTTPQueryValidator(spec)

    request = {
        'endpoint': '/endpoint/{path_param_1}/{path_param_2}',
        'method': 'post',
        'content_type': 'application/json',
        'headers': {'header_field': 'value'},
        'cookies': {'cookie_field': 'value'},
        'body': {'request_field': 'value'},
        'path_params': {'path_param_1': 'value', 'path_param_2': 'value'},
        'query_params': {'query_param_1': 'value', 'query_param_2': 'value'},
    }

    serialized_request = query_validator.request_handler(**request)

    assert serialized_request == request


def test_query_validators__response(fx_openapi_3_2_0, fx_open_spec):
    file_path = fx_openapi_3_2_0('query_validator.openapi.yaml')
    spec = fx_open_spec(file_path)
    query_validator = HTTPQueryValidator(spec)

    request = {
        'endpoint': '/endpoint/{path_param_1}/{path_param_2}',
        'method': 'post',
        'content_type': 'application/json',
        'status_code': '200',
        'body': {'response_field': 'value'},
    }

    serialized_request = query_validator.response_handler(**request)

    assert serialized_request == request
