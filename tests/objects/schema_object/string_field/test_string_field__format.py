import pytest

from schema_first.openapi.schemas.v3_1_1.schema_object_schema import SchemaObjectSchema


@pytest.mark.parametrize(
    'schema, fixture',
    [
        (SchemaObjectSchema, 'fx_field_string__binary'),
        (SchemaObjectSchema, 'fx_field_string__date'),
        (SchemaObjectSchema, 'fx_field_string__date_time'),
        (SchemaObjectSchema, 'fx_field_string__email'),
        (SchemaObjectSchema, 'fx_field_string__ipv4'),
        (SchemaObjectSchema, 'fx_field_string__ipv6'),
        (SchemaObjectSchema, 'fx_field_string__time'),
        (SchemaObjectSchema, 'fx_field_string__uri'),
        (SchemaObjectSchema, 'fx_field_string__uuid'),
    ],
)
def test_string_field__email(request, schema, fixture):
    schema().load(request.getfixturevalue(fixture))
