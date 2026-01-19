from marshmallow import fields
from marshmallow import validate

from ..base import BaseSchema
from ..constants import RE_SERVER_URL
from ..fields import DESCRIPTION_FIELD


class ExternalDocsSchema(BaseSchema):
    url = fields.String(
        required=True, validate=[validate.Regexp(RE_SERVER_URL), validate.Length(min=1)]
    )
    description = DESCRIPTION_FIELD
