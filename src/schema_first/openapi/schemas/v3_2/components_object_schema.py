from marshmallow import fields

from ..base import BaseSchema
from .responses_object_schema import ResponseObjectSchema
from .schema_object_schema import SchemaObjectSchema


class ComponentsObjectSchema(BaseSchema):
    responses = fields.Dict(
        keys=fields.String(), values=fields.Nested(ResponseObjectSchema, required=True)
    )
    schemas = fields.Dict(
        keys=fields.String(), values=fields.Nested(SchemaObjectSchema, required=True)
    )
