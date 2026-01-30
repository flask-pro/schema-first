from schema_first.openapi.schemas.v3_1_1.media_type_object_schema import MediaTypeObjectSchema


def test_media_type_object_schema__required(fx_media_type_object__required):
    MediaTypeObjectSchema().load(fx_media_type_object__required)


def test_media_type_object_schema__full(fx_media_type_object__full):
    MediaTypeObjectSchema().load(fx_media_type_object__full)
