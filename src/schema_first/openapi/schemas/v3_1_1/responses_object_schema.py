from marshmallow import fields

from ..base import BaseSchema
from ..fields import DESCRIPTION_FIELD
from ..fields import MEDIA_TYPE_FIELD
from .media_type_object_schema import MediaTypeObjectSchema


class ResponsesObjectSchema(BaseSchema):
    description = DESCRIPTION_FIELD
    content = fields.Dict(keys=MEDIA_TYPE_FIELD, values=fields.Nested(MediaTypeObjectSchema))
