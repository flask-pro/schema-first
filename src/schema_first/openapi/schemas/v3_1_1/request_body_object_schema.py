from marshmallow import fields
from schema_first.openapi.schemas._base import BaseSchema
from schema_first.openapi.schemas._fields import DESCRIPTION_FIELD
from schema_first.openapi.schemas._fields import MEDIA_TYPE_FIELD

from .media_type_object_schema import MediaTypeObjectSchema


class RequestBodyObject(BaseSchema):
    description = DESCRIPTION_FIELD
    content = fields.Dict(keys=MEDIA_TYPE_FIELD, values=fields.Nested(MediaTypeObjectSchema))
