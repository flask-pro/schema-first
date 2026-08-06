def test_media_type_object__any_binary(fx_openapi_3_2_0, fx_open_spec):
    file_path = fx_openapi_3_2_0('responses/binary.openapi.yaml')
    fx_open_spec(file_path)


def test_media_type_object__empty(fx_openapi_3_2_0, fx_open_spec):
    file_path = fx_openapi_3_2_0('responses/empty.openapi.yaml')
    fx_open_spec(file_path)
