from marshmallow.exceptions import ValidationError
import pytest

from schema_first.openapi.schemas.v3_1_1.schema_object_schema import SchemaObjectSchema


def test_server_schema_required(fx_schema_object__required):
    SchemaObjectSchema().load(fx_schema_object__required)


def test_server_schema_full(fx_schema_object__full):
    SchemaObjectSchema().load(fx_schema_object__full)


def test_server_schema__validate_mutual(fx_schema_object__full):
    fx_schema_object__full['identifier'] = 'Apache-2.0'
    with pytest.raises(ValidationError):
        SchemaObjectSchema().load(fx_schema_object__full)
