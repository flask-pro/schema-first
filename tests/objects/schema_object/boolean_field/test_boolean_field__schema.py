import pytest

from schema_first.openapi.schemas.v3_1_1.schema_object_schema import SchemaObjectSchema


@pytest.mark.parametrize('fixture', ['fx_field_boolean__required', 'fx_field_boolean__full'])
def test_boolean_field(request, fixture):
    SchemaObjectSchema().load(request.getfixturevalue(fixture))
