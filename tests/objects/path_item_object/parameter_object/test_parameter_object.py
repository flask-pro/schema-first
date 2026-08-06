from marshmallow import ValidationError
from marshmallow.schema import SchemaMeta
import pytest

from schema_first.openapi.exc import OpenAPIValidationError
from schema_first.openapi.schemas.v3_2.parameter_object_schema import ParameterObjectSchema


def test_parameter_required(fx_parameter_object_from_path_required):
    ParameterObjectSchema().load(fx_parameter_object_from_path_required)


def test_parameter_full(fx_parameter_object_from_path_full):
    ParameterObjectSchema().load(fx_parameter_object_from_path_full)


def test_parameter_object__all(fx_openapi_3_2_0, fx_open_spec):
    file_path = fx_openapi_3_2_0('parameters/all.yaml')
    spec = fx_open_spec(file_path)

    parameters = spec.reassembly_spec['paths']['/mini_endpoint/{path}']['get']['parameters']
    headers_schema = parameters['headers']['schema']
    assert isinstance(headers_schema, SchemaMeta)
    headers_schema().load({'header': 'test-headers', 'sub-header': 'test-headers'})

    cookies_schema = parameters['cookies']['schema']
    assert isinstance(parameters['cookies']['schema'], SchemaMeta)
    cookies_schema().load({'cookie': 'test-cookies', 'sub-cookie': 'test-cookies'})

    paths_schema = parameters['paths']['schema']
    assert isinstance(paths_schema, SchemaMeta)
    paths_schema().load({'path': 'test-paths'})

    queries_schema = parameters['queries']['schema']
    assert isinstance(parameters['queries']['schema'], SchemaMeta)
    queries_schema().load({'query': 'test-queries', 'sub-query': 'test-queries'})


def test_parameter_object__common(fx_openapi_3_2_0, fx_open_spec):
    file_path = fx_openapi_3_2_0('parameters/common.yaml')
    spec = fx_open_spec(file_path)

    parameters = spec.reassembly_spec['paths']['/mini_endpoint/{path}']['get']['parameters']
    headers_schema = parameters['headers']['schema']
    assert isinstance(headers_schema, SchemaMeta)
    headers_schema().load({'header': 'test-headers'})

    cookies_schema = parameters['cookies']['schema']
    assert isinstance(parameters['cookies']['schema'], SchemaMeta)
    cookies_schema().load({'cookie': 'test-cookies'})

    paths_schema = parameters['paths']['schema']
    assert isinstance(paths_schema, SchemaMeta)
    paths_schema().load({'path': 'test-paths'})

    queries_schema = parameters['queries']['schema']
    assert isinstance(parameters['queries']['schema'], SchemaMeta)
    queries_schema().load({'query': 'test-queries'})


def test_parameter_object__enum(fx_openapi_3_2_0, fx_open_spec):
    file_path = fx_openapi_3_2_0('parameters/enum.yaml')
    spec = fx_open_spec(file_path)

    parameters = spec.reassembly_spec['paths']['/mini_endpoint/{path}']['get']['parameters']

    headers_schema = parameters['headers']['schema']
    headers_schema().load({'header': 'header_param'})
    with pytest.raises(ValidationError) as e:
        headers_schema().load({'header': 'test-headers'})
    assert e.value.args[0] == {'header': ['Must be one of: header_param.']}

    cookies_schema = parameters['cookies']['schema']
    cookies_schema().load({'cookie': 'cookie_param'})
    with pytest.raises(ValidationError) as e:
        cookies_schema().load({'cookie': 'test-cookies'})
    assert e.value.args[0] == {'cookie': ['Must be one of: cookie_param.']}

    paths_schema = parameters['paths']['schema']
    paths_schema().load({'path': 'path_param'})
    with pytest.raises(ValidationError) as e:
        paths_schema().load({'path': 'test-paths'})
    assert e.value.args[0] == {'path': ['Must be one of: path_param.']}

    queries_schema = parameters['queries']['schema']
    queries_schema().load({'query': 'query_param'})
    with pytest.raises(ValidationError) as e:
        queries_schema().load({'query': 'test-queries'})
    assert e.value.args[0] == {'query': ['Must be one of: query_param.']}


def test_parameter_object__validate_path_parameters(fx_openapi_3_2_0, fx_open_spec):
    file_path = fx_openapi_3_2_0('parameters/validate_path_params.yaml')
    fx_open_spec(file_path, is_osv_validate=False)


@pytest.mark.parametrize('file_name', ['validate_path_params_invalid.yaml'])
def test_parameter_object__validate_path_parameters_invalid(
    fx_openapi_3_2_0, fx_open_spec, file_name
):
    file_path = fx_openapi_3_2_0(f'parameters/{file_name}')

    with pytest.raises(OpenAPIValidationError):
        fx_open_spec(file_path, is_osv_validate=False)
