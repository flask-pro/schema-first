import pytest

from schema_first.openapi.schemas.v3_1_1.schema_object_schema import SchemaObjectSchema


@pytest.mark.parametrize(
    'fixture',
    [
        'fx_field_string__binary',
        'fx_field_string__date',
        'fx_field_string__date_time',
        'fx_field_string__email',
        'fx_field_string__ipv4',
        'fx_field_string__ipv6',
        'fx_field_string__time',
        'fx_field_string__uri',
        'fx_field_string__uuid',
    ],
)
def test_string_field(request, fixture):
    SchemaObjectSchema().load(request.getfixturevalue(fixture))
