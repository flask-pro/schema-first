from marshmallow import fields
from marshmallow import validate

from ..base import BaseSchema
from ..base import DocStringFields
from .external_docs_schema import ExternalDocsSchema

kinds = ['audience', 'badge', 'nav']


class TagSchema(DocStringFields, BaseSchema):
    name = fields.String(required=True)
    externalDocs = fields.Nested(ExternalDocsSchema)
    parent = fields.String()
    kind = fields.String(validate=validate.OneOf(choices=kinds))
