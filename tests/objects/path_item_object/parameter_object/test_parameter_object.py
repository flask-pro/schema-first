from pathlib import Path

from marshmallow.schema import SchemaMeta

from schema_first.openapi.schemas.v3_2.parameter_object_schema import ParameterObjectSchema
from tests.conftest import tests_dir_abspath


def test_parameter_required(fx_parameter_object_from_path_required):
    ParameterObjectSchema().load(fx_parameter_object_from_path_required)


def test_parameter_full(fx_parameter_object_from_path_full):
    ParameterObjectSchema().load(fx_parameter_object_from_path_full)


def test_parameter_object__all(fx_open_spec):
    file_path = Path(tests_dir_abspath, '_contrib', 'specs', 'v3.2', 'parameters', 'all.yaml')
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


def test_parameter_object__common(fx_open_spec):
    file_path = Path(tests_dir_abspath, '_contrib', 'specs', 'v3.2', 'parameters', 'common.yaml')
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
