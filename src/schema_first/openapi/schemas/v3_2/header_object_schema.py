from marshmallow import fields

from schema_first.openapi.schemas.base import BaseSchema
from schema_first.openapi.schemas.fields import DESCRIPTION_FIELD
from schema_first.openapi.schemas.v3_2.example_object_schema import ExampleObjectSchema
from schema_first.openapi.schemas.v3_2.schema_object_schema import SchemaObjectSchema


class HeaderObjectSchema(BaseSchema):
    description = DESCRIPTION_FIELD
    required = fields.Boolean()
    deprecated = fields.Boolean()
    examples = fields.Dict(keys=fields.String(), values=fields.Nested(ExampleObjectSchema))
    schema = fields.Nested(SchemaObjectSchema)
