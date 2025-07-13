from marshmallow import fields
from marshmallow import validate
from schema_first.openapi.schemas._base import BaseSchema
from schema_first.openapi.schemas._constants import RE_SERVER_URL
from schema_first.openapi.schemas._fields import DESCRIPTION_FIELD

from .server_variable_object_schema import ServerVariableObjectSchema


class ServerSchema(BaseSchema):
    url = fields.String(
        required=True, validate=[validate.Regexp(RE_SERVER_URL), validate.Length(min=1)]
    )

    description = DESCRIPTION_FIELD

    variables = fields.Dict(
        keys=fields.String(), values=fields.Nested(ServerVariableObjectSchema, required=True)
    )
