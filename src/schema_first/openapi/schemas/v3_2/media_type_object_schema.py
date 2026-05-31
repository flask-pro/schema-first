from marshmallow import fields

from ..base import BaseSchema
from .example_object_schema import ExampleObjectSchema
from .schema_object_schema import SchemaObjectSchema


class MediaTypeObjectSchema(BaseSchema):
    schema = fields.Nested(SchemaObjectSchema)
    itemSchema = fields.Nested(SchemaObjectSchema)
    examples = fields.Dict(keys=fields.String(), values=fields.Nested(ExampleObjectSchema))
