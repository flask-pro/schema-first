from marshmallow import fields
from marshmallow import validate

from ..base import BaseSchema
from ..fields import DESCRIPTION_FIELD


class ServerVariableObjectSchema(BaseSchema):
    default = fields.String(required=True, validate=[validate.Length(min=1)])

    enum = fields.List(fields.String(validate=[validate.Length(min=1)]))
    description = DESCRIPTION_FIELD
