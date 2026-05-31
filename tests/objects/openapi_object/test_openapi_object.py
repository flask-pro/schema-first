from schema_first.openapi.schemas.v3_2.openapi_object_schema import OpenAPIObjectSchema


def test_openapi_schema_required(fx_openapi_object__required):
    OpenAPIObjectSchema().load(fx_openapi_object__required)


def test_openapi_schema_full(fx_openapi_object_full):
    OpenAPIObjectSchema().load(fx_openapi_object_full)
