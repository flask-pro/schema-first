from schema_first.openapi.schemas.v3_1_1.schema_object_schema import SchemaObjectSchema


def test_string_field__email(fx_field_string__email):
    SchemaObjectSchema().load(fx_field_string__email)
