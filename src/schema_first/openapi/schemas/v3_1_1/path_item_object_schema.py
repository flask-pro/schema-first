from marshmallow import fields

from ..base import BaseSchema
from ..base import DocStringFields
from .operation_object_schema import OperationObjectSchema
from .server_object_schema import ServerObjectSchema


class PathItemObjectSchema(DocStringFields, BaseSchema):
    get = fields.Nested(OperationObjectSchema)
    put = fields.Nested(OperationObjectSchema)
    post = fields.Nested(OperationObjectSchema)
    delete = fields.Nested(OperationObjectSchema)
    options = fields.Nested(OperationObjectSchema)
    head = fields.Nested(OperationObjectSchema)
    patch = fields.Nested(OperationObjectSchema)
    trace = fields.Nested(OperationObjectSchema)
    query = fields.Nested(OperationObjectSchema)
    servers = fields.Nested(ServerObjectSchema, many=True)
