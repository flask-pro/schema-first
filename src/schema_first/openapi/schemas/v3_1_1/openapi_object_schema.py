from marshmallow import fields
from marshmallow import validates_schema
from marshmallow import ValidationError

from ..base import BaseSchema
from ..constants import OPENAPI_VERSION_3_2
from ..fields import ENDPOINT_FIELD
from ..validators import VersionMatch
from .components_object_schema import ComponentsObjectSchema
from .external_docs_object_schema import ExternalDocsObjectSchema
from .info_object_schema import InfoObjectSchema
from .path_item_object_schema import PathItemObjectSchema
from .server_object_schema import ServerObjectSchema
from .tag_object_schema import TagObjectSchema


class OpenAPIObjectSchema(BaseSchema):
    openapi = fields.String(required=True, validate=VersionMatch(OPENAPI_VERSION_3_2))
    info = fields.Nested(InfoObjectSchema, required=True)
    paths = fields.Dict(
        required=True,
        keys=ENDPOINT_FIELD,
        values=fields.Nested(PathItemObjectSchema, required=True),
    )

    jsonSchemaDialect = fields.URL()

    servers = fields.Nested(ServerObjectSchema, many=True)
    components = fields.Nested(ComponentsObjectSchema)
    tags = fields.Nested(TagObjectSchema, many=True)
    externalDocs = fields.Nested(ExternalDocsObjectSchema)

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
