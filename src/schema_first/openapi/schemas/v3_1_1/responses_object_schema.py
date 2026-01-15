from marshmallow import fields

from ..base import BaseSchema
from ..base import DocStringFields
from ..fields import MEDIA_TYPE_FIELD
from .media_type_object_schema import MediaTypeObjectSchema


class ResponsesObjectSchema(DocStringFields, BaseSchema):
    content = fields.Dict(keys=MEDIA_TYPE_FIELD, values=fields.Nested(MediaTypeObjectSchema))
