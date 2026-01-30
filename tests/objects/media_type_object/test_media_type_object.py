from schema_first.openapi.schemas.v3_1_1.media_type_object_schema import MediaTypeObjectSchema


def test_media_type_object_schema_required(fx_media_type_object_required):
    MediaTypeObjectSchema().load(fx_media_type_object_required)


def test_media_type_object_schema_full(fx_media_type_object_full):
    MediaTypeObjectSchema().load(fx_media_type_object_full)
