def test_object_field(fx_openapi_3_2_0, fx_open_spec):
    file_path = fx_openapi_3_2_0('schemas/object.yaml')
    spec = fx_open_spec(file_path)

    schema = spec.reassembly_spec['paths']['/endpoint']['get']['responses']['200']['content'][
        'application/json'
    ]['schema']
    schema().load({'nested_field': {'field': 'test'}})
