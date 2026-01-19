from marshmallow import fields

from ..base import BaseSchema
from ..constants import OPENAPI_VERSION_3_2
from ..fields import ENDPOINT_FIELD
from ..validators import VersionMatch
from .components_object_schema import ComponentsObjectSchema
from .info_schema import InfoSchema
from .path_item_object_schema import PathItemObjectSchema
from .server_schema import ServerSchema


class OpenAPIObjectSchema(BaseSchema):
    openapi = fields.String(required=True, validate=VersionMatch(OPENAPI_VERSION_3_2))
    info = fields.Nested(InfoSchema, required=True)
    paths = fields.Dict(
        required=True,
        keys=ENDPOINT_FIELD,
        values=fields.Nested(PathItemObjectSchema, required=True),
    )

    jsonSchemaDialect = fields.URL()

    servers = fields.Nested(ServerSchema, many=True)
    components = fields.Nested(ComponentsObjectSchema)
    externalDocs = fields.Nested(ServerSchema)
