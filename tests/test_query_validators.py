import pytest

from schema_first.query.exceptions import EndpointValidation
from schema_first.query.exceptions import QueryValidatorException
from schema_first.query.exceptions import ResponseValidation
from schema_first.query.validator import HTTPQueryValidator


def test_query_validators__request(fx_openapi_3_2_0, fx_open_spec):
    file_path = fx_openapi_3_2_0('query_validator/openapi.yaml')
    spec = fx_open_spec(file_path)
    query_validator = HTTPQueryValidator(spec)

    request = {
        'endpoint': '/endpoint/{path_param_1}/{path_param_2}',
        'method': 'post',
        'content_type': 'application/json',
        'headers': {'header_field': 'value'},
        'cookies': {'cookie_field': 'value'},
        'body': {'request_field': 'value'},
        'paths': {'path_param_1': 'value', 'path_param_2': 'value'},
        'queries': {'query_param_1': 'value', 'query_param_2': 'value'},
    }

    serialized_request = query_validator.request_handler(**request)

    assert serialized_request == request


def test_query_validators__request__empty_body_without_request_body(fx_openapi_3_2_0, fx_open_spec):
    file_path = fx_openapi_3_2_0('query_validator/no_request_body.yaml')
    spec = fx_open_spec(file_path)
    query_validator = HTTPQueryValidator(spec)

    request = {'endpoint': '/endpoint', 'method': 'get'}

    serialized_request = query_validator.request_handler(**request)

    assert serialized_request == request


def test_query_validators__request__empty_body_with_request_body(fx_openapi_3_2_0, fx_open_spec):
    file_path = fx_openapi_3_2_0('query_validator/request_body.yaml')
    spec = fx_open_spec(file_path)
    query_validator = HTTPQueryValidator(spec)

    request = {'endpoint': '/endpoint', 'method': 'post'}

    serialized_request = query_validator.request_handler(**request)

    assert serialized_request == request


def test_query_validators__request__bad_endpoint(fx_openapi_3_2_0, fx_open_spec):
    file_path = fx_openapi_3_2_0('query_validator/openapi.yaml')
    spec = fx_open_spec(file_path)
    query_validator = HTTPQueryValidator(spec)

    request = {'endpoint': '/non_exist', 'method': 'post', 'content_type': 'application/json'}

    with pytest.raises(EndpointValidation) as exc:
        query_validator.request_handler(**request)

    assert exc.value.args == ('Path </non_exist> not in OpenAPI specification.',)


@pytest.mark.parametrize(
    ('spec', 'data'),
    [
        ('no_params.yaml', {'headers': {'field': 'value'}}),
        ('only_headers.yaml', {'cookies': {'field': 'value'}}),
        ('only_headers.yaml', {'paths': {'field': 'value'}}),
        ('only_headers.yaml', {'queries': {'field': 'value'}}),
        ('only_headers.yaml', {'content_type': 'application/json', 'body': {'field': 'value'}}),
        ('only_query.yaml', {'headers': {'field': 'value'}}),
        ('only_headers.yaml', {'body': {'field': 'value'}}),
    ],
)
def test_query_validators__request_errors(fx_openapi_3_2_0, fx_open_spec, spec, data):
    file_path = fx_openapi_3_2_0(f'query_validator/{spec}')
    spec = fx_open_spec(file_path)
    query_validator = HTTPQueryValidator(spec)

    request = {
        'endpoint': '/endpoint',
        'method': 'post',
        **data,
    }

    with pytest.raises(QueryValidatorException):
        query_validator.request_handler(**request)


def test_query_validators__response(fx_openapi_3_2_0, fx_open_spec):
    file_path = fx_openapi_3_2_0('query_validator/openapi.yaml')
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


def test_query_validators__response__empty_body_in_spec(fx_openapi_3_2_0, fx_open_spec):
    file_path = fx_openapi_3_2_0('query_validator/empty_body.yaml')
    spec = fx_open_spec(file_path)
    query_validator = HTTPQueryValidator(spec)

    request = {'endpoint': '/endpoint', 'method': 'get', 'status_code': '204'}

    serialized_request = query_validator.response_handler(**request)

    assert serialized_request == request


def test_query_validators__response__empty_body_in_spec_error(fx_openapi_3_2_0, fx_open_spec):
    file_path = fx_openapi_3_2_0('query_validator/empty_body.yaml')
    spec = fx_open_spec(file_path)
    query_validator = HTTPQueryValidator(spec)

    request = {
        'endpoint': '/endpoint',
        'method': 'get',
        'content_type': 'application/json',
        'status_code': '204',
        'body': {'field': 'value'},
    }

    with pytest.raises(ResponseValidation):
        query_validator.response_handler(**request)
