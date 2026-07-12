from pathlib import Path

from openapi_spec_validator import validate as osv_validate
from openapi_spec_validator.readers import read_from_filename

from src.schema_first.specification import Specification
from tests.conftest import tests_dir_abspath


def test_array_field():
    file_path = Path(tests_dir_abspath, '_contrib', 'specs', 'v3.2', 'array', 'all.yaml')
    spec_as_dict, base_uri = read_from_filename(file_path)
    osv_validate(spec_as_dict, base_uri=base_uri)

    spec = Specification(file_path)
    spec.load()

    schema = spec.reassembly_spec['paths']['/mini_endpoint']['post']['requestBody']['content'][
        'application/json'
    ]['schema']
    schema().load({'array': ['test']})

    schema = spec.reassembly_spec['paths']['/mini_endpoint']['post']['responses']['201']['content'][
        'application/json'
    ]['schema']
    schema().load({'array': [{'field': 'test'}]})
