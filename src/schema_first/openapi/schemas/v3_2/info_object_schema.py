from marshmallow import fields
from marshmallow import validate

from schema_first.openapi.schemas.base import BaseSchema
from schema_first.openapi.schemas.base import DocStringFields
from schema_first.openapi.schemas.constants import RE_VERSION
from schema_first.openapi.schemas.v3_2.contact_object_schema import ContactObjectSchema
from schema_first.openapi.schemas.v3_2.license_object_schema import LicenseObjectSchema


class InfoObjectSchema(DocStringFields, BaseSchema):
    title = fields.String(required=True)
    version = fields.String(required=True, validate=validate.Regexp(RE_VERSION))

    termsOfService = fields.String()

    contact = fields.Nested(ContactObjectSchema)
    license = fields.Nested(LicenseObjectSchema)
