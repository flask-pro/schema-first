from pathlib import Path

from tests.conftest import tests_dir_abspath


def test_array_field(fx_open_spec):
    file_path = Path(tests_dir_abspath, '_contrib', 'specs', 'v3.2', 'array', 'all.yaml')
    spec = fx_open_spec(file_path)

    schema = spec.reassembly_spec['paths']['/mini_endpoint']['post']['requestBody']['content'][
        'application/json'
    ]['schema']
    schema().load({'array': ['test']})

    schema = spec.reassembly_spec['paths']['/mini_endpoint']['post']['responses']['201']['content'][
        'application/json'
    ]['schema']
    schema().load({'array': [{'field': 'test'}]})
