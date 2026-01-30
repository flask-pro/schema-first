from schema_first.openapi.schemas.v3_1_1.path_item_object_schema import PathItemObjectSchema


def test_path_item_schema_required(fx_path_item_object__required):
    PathItemObjectSchema().load(fx_path_item_object__required)


def test_path_item_schema_full(fx_path_item_object__full):
    PathItemObjectSchema().load(fx_path_item_object__full)
