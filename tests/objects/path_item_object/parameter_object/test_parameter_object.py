from pathlib import Path

from marshmallow.schema import SchemaMeta
from openapi_spec_validator import validate as osv_validate
from openapi_spec_validator.readers import read_from_filename

from schema_first.openapi.schemas.v3_2.parameter_object_schema import ParameterObjectSchema
from src.schema_first.specification import Specification
from tests.conftest import tests_dir_abspath


def test_parameter_required(fx_parameter_object_from_path_required):
    ParameterObjectSchema().load(fx_parameter_object_from_path_required)


def test_parameter_full(fx_parameter_object_from_path_full):
    ParameterObjectSchema().load(fx_parameter_object_from_path_full)


def test_parameter_object__all_place():
    file_path = Path(tests_dir_abspath, '_contrib', 'specs', 'v3.2', 'parameters', 'all.yaml')
    spec_as_dict, base_uri = read_from_filename(file_path)
    osv_validate(spec_as_dict, base_uri=base_uri)

    spec = Specification(file_path)
    spec.load()

    parameters = spec.reassembly_spec['paths']['/mini_endpoint/{uuid}']['get']['parameters']
    assert isinstance(parameters['headers']['schema'], SchemaMeta)
    assert isinstance(parameters['cookies']['schema'], SchemaMeta)
    assert isinstance(parameters['paths']['schema'], SchemaMeta)
    assert isinstance(parameters['queries']['schema'], SchemaMeta)
