import pytest

from schema_first.openapi.schemas.v3_1_1.schema_object_schema import SchemaObjectSchema


@pytest.mark.parametrize('fixture', ['fx_field_integer__int32', 'fx_field_integer__int64'])
def test_integer_field_formats(request, fixture):
    SchemaObjectSchema().load(request.getfixturevalue(fixture))
