from schema_first.openapi.schemas.v3_2.components_object_schema import ComponentsObjectSchema


def test_components_schema_full(fx_components_object_full):
    ComponentsObjectSchema().load(fx_components_object_full)
