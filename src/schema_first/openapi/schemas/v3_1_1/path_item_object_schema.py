from marshmallow import fields

from ..base import BaseSchema
from ..base import DocStringFields
from .operation_object_schema import OperationObjectSchema


class PathItemObjectSchema(DocStringFields, BaseSchema):
    get = fields.Nested(OperationObjectSchema, metadata={'q': 1})
    post = fields.Nested(OperationObjectSchema)
