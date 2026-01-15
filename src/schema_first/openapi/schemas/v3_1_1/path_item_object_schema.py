from marshmallow import fields

from ..base import BaseSchema
from ..base import DocStringFields
from .operation_object_schema import OperationObjectSchema


class PathItemObjectSchema(DocStringFields, BaseSchema):
    get = fields.Nested(OperationObjectSchema)
    post = fields.Nested(OperationObjectSchema)
