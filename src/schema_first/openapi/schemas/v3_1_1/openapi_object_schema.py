from marshmallow import fields
from marshmallow import validates_schema
from marshmallow import ValidationError

from ..base import BaseSchema
from ..constants import OPENAPI_VERSION_3_2
from ..fields import ENDPOINT_FIELD
from ..validators import VersionMatch
from .components_object_schema import ComponentsObjectSchema
from .external_docs_schema import ExternalDocsSchema
from .info_schema import InfoSchema
from .path_item_object_schema import PathItemObjectSchema
from .server_schema import ServerSchema
from .tag_schema import TagSchema


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
    tags = fields.Nested(TagSchema, many=True)
    externalDocs = fields.Nested(ExternalDocsSchema)

    @validates_schema
    def validate_tags(self, data, **kwargs):
        if tags := data.get('tags'):
            names = []
            parents = []

            for tag in tags:
                names.append(tag['name'])

                if parent := tag.get('parent'):
                    parents.append(parent)

            parents_not_in_names = [parent for parent in parents if parent not in names]
            if parents_not_in_names:
                raise ValidationError(f'Parents <{names}> not exist in names tags <{names}>.')
