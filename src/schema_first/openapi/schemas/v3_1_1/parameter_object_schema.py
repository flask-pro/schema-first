from marshmallow import fields
from marshmallow import validate

from ..base import BaseSchema
from ..constants import LOCATION_PARAMETER
from ..fields import DESCRIPTION_FIELD
from .example_object_schema import ExampleObjectSchema


class ParameterObjectSchema(BaseSchema):
    name = fields.String(required=True)
    in_ = fields.String(required=True, data_key='in', validate=validate.OneOf(LOCATION_PARAMETER))

    description = DESCRIPTION_FIELD
    required = fields.Boolean()
    deprecated = fields.Boolean()
    examples = fields.Dict(keys=fields.String(), values=fields.Nested(ExampleObjectSchema))
