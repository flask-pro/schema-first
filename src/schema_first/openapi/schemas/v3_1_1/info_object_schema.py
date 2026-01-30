from marshmallow import fields
from marshmallow import validate

from ..base import BaseSchema
from ..base import DocStringFields
from ..constants import RE_VERSION
from .contact_object_schema import ContactObjectSchema
from .license_object_schema import LicenseObjectSchema


class InfoObjectSchema(DocStringFields, BaseSchema):
    title = fields.String(required=True)
    version = fields.String(required=True, validate=validate.Regexp(RE_VERSION))

    termsOfService = fields.String()

    contact = fields.Nested(ContactObjectSchema)
    license = fields.Nested(LicenseObjectSchema)
