from marshmallow import fields

from ..base import BaseSchema
from .responses_object_schema import ResponsesObjectSchema
from .schema_object_schema import SchemaObjectSchema


class ComponentsObjectSchema(BaseSchema):
    responses = fields.Dict(
        keys=fields.String(), values=fields.Nested(ResponsesObjectSchema, required=True)
    )
    schemas = fields.Dict(
        keys=fields.String(), values=fields.Nested(SchemaObjectSchema, required=True)
    )
