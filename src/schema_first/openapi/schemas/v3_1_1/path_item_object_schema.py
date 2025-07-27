from marshmallow import fields

from ..base import BaseSchema
from .operation_object_schema import OperationObjectSchema


class PathItemObjectSchema(BaseSchema):
    get = fields.Nested(OperationObjectSchema)
    post = fields.Nested(OperationObjectSchema)
