from marshmallow import fields
from marshmallow import validate

from ..base import BaseSchema
from ..base import DocStringFields
from .external_docs_object_schema import ExternalDocsObjectSchema

kinds = ['audience', 'badge', 'nav']


class TagObjectSchema(DocStringFields, BaseSchema):
    name = fields.String(required=True)
    externalDocs = fields.Nested(ExternalDocsObjectSchema)
    parent = fields.String()
    kind = fields.String(validate=validate.OneOf(choices=kinds))
