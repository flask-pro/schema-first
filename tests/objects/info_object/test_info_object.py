from schema_first.openapi.schemas.v3_2.info_object_schema import InfoObjectSchema


def test_info_object_schema_required(fx_info_object_required):
    InfoObjectSchema().load(fx_info_object_required)


def test_info_object_schema_full(fx_info_object_full):
    InfoObjectSchema().load(fx_info_object_full)
