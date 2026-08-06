from marshmallow import fields
from marshmallow import validate

from schema_first.openapi.schemas.base import BaseSchema
from schema_first.openapi.schemas.constants import RE_SERVER_URL
from schema_first.openapi.schemas.fields import DESCRIPTION_FIELD


class ExternalDocsObjectSchema(BaseSchema):
    url = fields.String(
        required=True, validate=[validate.Regexp(RE_SERVER_URL), validate.Length(min=1)]
    )
    description = DESCRIPTION_FIELD
