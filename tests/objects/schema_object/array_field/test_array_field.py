def test_array_field(fx_openapi_3_2_0, fx_open_spec):
    file_path = fx_openapi_3_2_0('schemas/array.yaml')
    spec = fx_open_spec(file_path)

    schema = spec.reassembly_spec['paths']['/mini_endpoint']['post']['requestBody']['content'][
        'application/json'
    ]['schema']
    schema().load({'array': ['test']})

    schema = spec.reassembly_spec['paths']['/mini_endpoint']['post']['responses']['201']['content'][
        'application/json'
    ]['schema']
    schema().load({'array': [{'field': 'test'}]})
