from marshmallow import fields

from schema_first.openapi.schemas.base import BaseSchema
from schema_first.openapi.schemas.v3_2.example_object_schema import ExampleObjectSchema
from schema_first.openapi.schemas.v3_2.header_object_schema import HeaderObjectSchema
from schema_first.openapi.schemas.v3_2.media_type_object_schema import MediaTypeObjectSchema
from schema_first.openapi.schemas.v3_2.parameter_object_schema import ParameterObjectSchema
from schema_first.openapi.schemas.v3_2.path_item_object_schema import PathItemObjectSchema
from schema_first.openapi.schemas.v3_2.responses_object_schema import ResponseObjectSchema
from schema_first.openapi.schemas.v3_2.schema_object_schema import SchemaObjectSchema


class ComponentsObjectSchema(BaseSchema):
    responses = fields.Dict(
        keys=fields.String(), values=fields.Nested(ResponseObjectSchema, required=True)
    )
    schemas = fields.Dict(
        keys=fields.String(), values=fields.Nested(SchemaObjectSchema, required=True)
    )
    parameters = fields.Dict(
        keys=fields.String(), values=fields.Nested(ParameterObjectSchema, required=True)
    )
    examples = fields.Dict(
        keys=fields.String(), values=fields.Nested(ExampleObjectSchema, required=True)
    )
    headers = fields.Dict(
        keys=fields.String(), values=fields.Nested(HeaderObjectSchema, required=True)
    )
    pathItems = fields.Dict(
        keys=fields.String(), values=fields.Nested(PathItemObjectSchema, required=True)
    )
    mediaTypes = fields.Dict(
        keys=fields.String(), values=fields.Nested(MediaTypeObjectSchema, required=True)
    )
