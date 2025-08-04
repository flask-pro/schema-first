import pytest

from src.schema_first.loaders.exc import YAMLReaderError
from src.schema_first.loaders.yaml_loader import load_from_yaml


def test_loaders__yaml__multiple__response_ref(fx_spec_required, fx_spec_as_file):
    endpoint_spec = {'endpoint': fx_spec_required['paths']['/endpoint']}
    endpoint_spec['endpoint']['get']['responses']['200']['content']['application/json']['schema'][
        'properties'
    ]['message'] = {'$ref': '#/components/schemas/Message'}
    endpoint_spec['components'] = {'schemas': {'Message': {'type': 'string'}}}
    endpoint_spec_file = fx_spec_as_file(endpoint_spec, file_name='endpoint.yaml')

    fx_spec_required['paths']['/endpoint'] = {'$ref': f'{endpoint_spec_file.name}#/endpoint'}
    spec_file = fx_spec_as_file(fx_spec_required)
    spec_obj = load_from_yaml(spec_file)

    assert spec_obj['paths']['/endpoint'].get('$ref') is None
    assert spec_obj['paths']['/endpoint']['get']['responses']['200']['content']['application/json'][
        'schema'
    ]['properties']['message'] == {'type': 'string'}


def test_loader__internal__multiple__non_exist_file(fx_spec_required, fx_spec_as_file):
    non_exist_file_name = 'non_exist_file.yaml'
    fx_spec_required['paths']['/endpoint'] = {'$ref': f'{non_exist_file_name}#/endpoint'}
    spec_file = fx_spec_as_file(fx_spec_required)

    with pytest.raises(YAMLReaderError) as e:
        load_from_yaml(spec_file)

    assert str(e.value) == f'No such file or directory: <{non_exist_file_name}>'
