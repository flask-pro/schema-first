import pytest

from schema_first.openapi.schemas.v3_1_1.schema_object_schema import SchemaObjectSchema


@pytest.mark.parametrize('fixture', ['fx_field_number__float', 'fx_field_number__double'])
def test_number_field_formats(request, fixture):
    SchemaObjectSchema().load(request.getfixturevalue(fixture))
