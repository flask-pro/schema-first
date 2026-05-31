from marshmallow import fields

from ..base import BaseSchema
from ..base import DocStringFields
from ..fields import HEADER_NAME_FIELD
from ..fields import MEDIA_TYPE_FIELD
from .header_object_schema import HeaderObjectSchema
from .media_type_object_schema import MediaTypeObjectSchema


class ResponseObjectSchema(DocStringFields, BaseSchema):
    content = fields.Dict(keys=MEDIA_TYPE_FIELD, values=fields.Nested(MediaTypeObjectSchema))
    headers = fields.Dict(keys=HEADER_NAME_FIELD, values=fields.Nested(HeaderObjectSchema))
