from marshmallow import fields
from marshmallow import validates_schema
from marshmallow import ValidationError

from ..base import BaseSchema


class LicenseSchema(BaseSchema):
    name = fields.String(required=True)

    identifier = fields.String()
    url = fields.URL()

    @validates_schema
    def validate_exclusive(self, data, **kwargs) -> None:
        if 'identifier' in data and 'url' in data:
            raise ValidationError(
                'The <identifier> field is mutually exclusive of the <url> field.'
            )
