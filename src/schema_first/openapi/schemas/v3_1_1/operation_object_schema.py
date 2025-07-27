from marshmallow import fields

from ..base import BaseSchema
from ..fields import HTTP_CODE_FIELD
from .request_body_object_schema import RequestBodyObject
from .responses_object_schema import ResponsesObjectSchema


class OperationObjectSchema(BaseSchema):
    operation_id = fields.String(data_key='operationId')
    requestBody = fields.Nested(RequestBodyObject)
    responses = fields.Dict(keys=HTTP_CODE_FIELD, values=fields.Nested(ResponsesObjectSchema))
