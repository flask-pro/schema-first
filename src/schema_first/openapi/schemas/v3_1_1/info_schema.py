from marshmallow import fields
from marshmallow import validate

from ..base import BaseSchema
from ..base import DocStringFields
from ..constants import RE_VERSION
from .contact_schema import ContactSchema
from .license_schema import LicenseSchema


class InfoSchema(DocStringFields, BaseSchema):
    title = fields.String(required=True)
    version = fields.String(required=True, validate=validate.Regexp(RE_VERSION))

    termsOfService = fields.String()

    contact = fields.Nested(ContactSchema)
    license = fields.Nested(LicenseSchema)
