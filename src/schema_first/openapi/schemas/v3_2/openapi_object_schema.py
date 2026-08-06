import re

from marshmallow import fields
from marshmallow import post_load
from marshmallow import validates_schema
from marshmallow import ValidationError

from schema_first.openapi.schemas.base import BaseSchema
from schema_first.openapi.schemas.constants import OPENAPI_VERSION_3_2
from schema_first.openapi.schemas.fields import ENDPOINT_FIELD
from schema_first.openapi.schemas.v3_2.components_object_schema import ComponentsObjectSchema
from schema_first.openapi.schemas.v3_2.external_docs_object_schema import ExternalDocsObjectSchema
from schema_first.openapi.schemas.v3_2.info_object_schema import InfoObjectSchema
from schema_first.openapi.schemas.v3_2.path_item_object_schema import PathItemObjectSchema
from schema_first.openapi.schemas.v3_2.server_object_schema import ServerObjectSchema
from schema_first.openapi.schemas.v3_2.tag_object_schema import TagObjectSchema
from schema_first.openapi.schemas.validators import VersionMatch


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

    @post_load
    def validate_path_parameter(self, data, **kwargs) -> None:
        endpoints = data['paths']
        for endpoint, path_item in endpoints.items():
            path_params_names = set()

            common_params = path_item.get('parameters')
            if common_params:
                for param in common_params:
                    if param['in_'] == 'path':
                        path_params_names.update([param['name']])

            for method, method_content in path_item.items():
                if method not in ['post', 'get', 'update', 'patch', 'delete']:
                    continue

                params_from_endpoint = method_content.get('parameters')
                if params_from_endpoint:
                    for param in params_from_endpoint:
                        if param['in_'] == 'path':
                            path_params_names.update([param['name']])

            if components := data.get('components'):
                params_from_components = components.get('parameters')
                if params_from_components:
                    for param in params_from_components.values():
                        if param['in_'] == 'path':
                            path_params_names.update([param['name']])

            param_names_from_path = re.findall(r'\{(.*?)}', endpoint)
            if param_names_from_path:
                if not set(param_names_from_path).issubset(path_params_names):
                    raise ValidationError(
                        f'Parameters from <{param_names_from_path}> not in <{endpoint}>'
                        f' and not in </components/parameters>.'
                    )
