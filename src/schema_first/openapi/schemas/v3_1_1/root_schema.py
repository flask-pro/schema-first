from marshmallow import fields
from marshmallow import validate

from ..base import BaseSchema
from ..constants import OPENAPI_VERSION
from ..fields import ENDPOINT_FIELD
from .components_object_schema import ComponentsObjectSchema
from .info_schema import InfoSchema
from .path_item_object_schema import PathItemObjectSchema
from .server_schema import ServerSchema


class RootSchema(BaseSchema):
    openapi = fields.String(required=True, validate=validate.Equal(OPENAPI_VERSION))
    info = fields.Nested(InfoSchema, required=True)
    paths = fields.Dict(
        required=True,
        keys=ENDPOINT_FIELD,
        values=fields.Nested(PathItemObjectSchema, required=True),
    )

    jsonSchemaDialect = fields.URL()

    servers = fields.Nested(ServerSchema, many=True)
    components = fields.Nested(ComponentsObjectSchema)
