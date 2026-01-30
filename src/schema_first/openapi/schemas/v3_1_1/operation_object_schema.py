from marshmallow import fields

from ..base import BaseSchema
from ..base import DocStringFields
from ..fields import HTTP_CODE_FIELD
from .external_docs_object_schema import ExternalDocsObjectSchema
from .request_body_object_schema import RequestBodyObject
from .responses_object_schema import ResponseObjectSchema
from .server_object_schema import ServerObjectSchema


class OperationObjectSchema(DocStringFields, BaseSchema):
    tags = fields.List(fields.String)
    externalDocs = fields.Nested(ExternalDocsObjectSchema)
    operationId = fields.String()
    requestBody = fields.Nested(RequestBodyObject)
    responses = fields.Dict(keys=HTTP_CODE_FIELD, values=fields.Nested(ResponseObjectSchema))
    deprecated = fields.Boolean()
    servers = fields.Nested(ServerObjectSchema, many=True)
