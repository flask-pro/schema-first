from marshmallow import fields
from marshmallow import validate
from schema_first.openapi.schemas._base import BaseSchema
from schema_first.openapi.schemas._fields import DESCRIPTION_FIELD


class ServerVariableObjectSchema(BaseSchema):
    enum = fields.List(fields.String(validate=[validate.Length(min=1)]))
    default = fields.String(required=True, validate=[validate.Length(min=1)])
    description = DESCRIPTION_FIELD
