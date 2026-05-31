from marshmallow import fields

from ..base import BaseSchema
from ..fields import DESCRIPTION_FIELD
from .example_object_schema import ExampleObjectSchema
from .schema_object_schema import SchemaObjectSchema


class HeaderObjectSchema(BaseSchema):
    description = DESCRIPTION_FIELD
    required = fields.Boolean()
    deprecated = fields.Boolean()
    examples = fields.Dict(keys=fields.String(), values=fields.Nested(ExampleObjectSchema))
    schema = fields.Nested(SchemaObjectSchema)
