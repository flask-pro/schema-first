def test_loaders__yaml__multiple__parameters(fx_spec_minimal, fx_spec_as_file):
    endpoint_spec = {'endpoint': fx_spec_minimal['paths']['/endpoint']}
    endpoint_spec['endpoint']['parameters'] = [{'$ref': '#/components/parameters/path_param'}]
    endpoint_spec['components'] = {
        'parameters': {
            'path_param': {
                'name': 'path_param',
                'in': 'path',
                'required': True,
                'schema': {'type': 'string', 'enum': ['path_param']},
            }
        }
    }
    endpoint_spec_file = fx_spec_as_file(endpoint_spec, file_name='endpoint.yaml')

    fx_spec_minimal['paths']['/endpoint/{path_param}'] = {
        '$ref': f'{endpoint_spec_file.name}#/endpoint'
    }
    fx_spec_minimal['paths'].pop('/endpoint')

    fx_spec_as_file(fx_spec_minimal)
