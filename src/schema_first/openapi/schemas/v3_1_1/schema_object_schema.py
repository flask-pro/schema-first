from marshmallow import fields
from marshmallow import validate

from ..base import BaseSchema
from ..constants import FORMATS
from ..constants import TYPES


class SchemaObjectSchema(BaseSchema):
    type = fields.String(required=True, validate=validate.OneOf(TYPES))

    format = fields.String(validate=validate.OneOf(FORMATS))
    pattern = fields.String()

    properties = fields.Dict(
        keys=fields.String(required=True), values=fields.Nested(lambda: SchemaObjectSchema())
    )
