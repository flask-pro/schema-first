from marshmallow import fields
from marshmallow import validate
from schema_first.openapi.schemas._base import BaseSchema
from schema_first.openapi.schemas._constants import RE_VERSION
from schema_first.openapi.schemas._fields import DESCRIPTION_FIELD
from schema_first.openapi.schemas._fields import SUMMARY_FIELD

from .contact_schema import ContactSchema
from .license_schema import LicenseSchema


class InfoSchema(BaseSchema):
    title = fields.String(required=True)
    version = fields.String(required=True, validate=validate.Regexp(RE_VERSION))

    summary = SUMMARY_FIELD
    description = DESCRIPTION_FIELD
    terms_of_service = fields.String(data_key='termsOfService')

    contact = fields.Nested(ContactSchema)
    license = fields.Nested(LicenseSchema)
