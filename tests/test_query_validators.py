import pytest

from schema_first.query.exceptions import EndpointValidation
from schema_first.query.exceptions import QueryValidatorException
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
        'path_params': {'path_param_1': 'value', 'path_param_2': 'value'},
        'query_params': {'query_param_1': 'value', 'query_param_2': 'value'},
    }

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
    ('spec', 'data', 'msg'),
    [
        (
            'no_params.yaml',
            {'headers': {'field': 'value'}},
            'Parameters for </endpoint> not in OpenAPI specification.',
        ),
        (
            'only_headers.yaml',
            {'cookies': {'field': 'value'}},
            "Cookies <{'field': 'value'}> not in OpenAPI specification.",
        ),
        (
            'only_headers.yaml',
            {'path_params': {'field': 'value'}},
            "Path parameters <{'field': 'value'}> not in OpenAPI specification.",
        ),
        (
            'only_headers.yaml',
            {'query_params': {'field': 'value'}},
            "Query parameters <{'field': 'value'}> not in OpenAPI specification.",
        ),
        (
            'only_headers.yaml',
            {'content_type': 'application/json', 'body': {'field': 'value'}},
            'Content type <application/json> not in OpenAPI specification.',
        ),
        (
            'only_query.yaml',
            {'headers': {'field': 'value'}},
            "Headers <{'field': 'value'}> not in OpenAPI specification.",
        ),
        (
            'only_headers.yaml',
            {'body': {'field': 'value'}},
            '<content_type> and <body> should be passed together.',
        ),
    ],
)
def test_query_validators__request_errors(fx_openapi_3_2_0, fx_open_spec, spec, data, msg):
    file_path = fx_openapi_3_2_0(f'query_validator/{spec}')
    spec = fx_open_spec(file_path)
    query_validator = HTTPQueryValidator(spec)

    request = {
        'endpoint': '/endpoint',
        'method': 'post',
        **data,
    }

    with pytest.raises(QueryValidatorException) as exc:
        query_validator.request_handler(**request)

    assert exc.value.args == (msg,)


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
