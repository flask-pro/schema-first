from marshmallow import fields
from schema_first.openapi.schemas._base import BaseSchema

from .schema_object_schema import SchemaObjectSchema


class MediaTypeObjectSchema(BaseSchema):
    schema = fields.Nested(SchemaObjectSchema)
