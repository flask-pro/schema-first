from marshmallow import fields
from marshmallow import validate
from marshmallow import validates_schema
from marshmallow import ValidationError

from schema_first.openapi.schemas.base import BaseSchema
from schema_first.openapi.schemas.constants import API_KEY_LOCATIONS
from schema_first.openapi.schemas.constants import HTTP_AUTH_SCHEMES
from schema_first.openapi.schemas.constants import TYPE_AUTH_METHODS
from schema_first.openapi.schemas.fields import DESCRIPTION_FIELD


class SecuritySchemeObjectSchema(BaseSchema):
    type = fields.String(required=True, validate=validate.OneOf(TYPE_AUTH_METHODS))

    description = DESCRIPTION_FIELD
    name = fields.String()
    in_ = fields.String(data_key='in', validate=validate.OneOf(API_KEY_LOCATIONS))
    scheme = fields.String(validate=validate.OneOf(HTTP_AUTH_SCHEMES))
    bearerFormat = fields.String()
    deprecated = fields.Boolean()

    @validates_schema
    def validate_http_scheme_required(self, data, **kwargs):
        if data['type'] == 'http' and not data.get('scheme'):
            raise ValidationError('Field <scheme> required for type <http>.')

    @validates_schema
    def validate_api_key_name_required(self, data, **kwargs):
        if data['type'] == 'apiKey' and not data.get('name'):
            raise ValidationError('Field <name> required for type <apiKey>.')

    @validates_schema
    def validate_api_key_in_required(self, data, **kwargs):
        if data['type'] == 'apiKey' and not data.get('in_'):
            raise ValidationError('Field <in> required for type <apiKey>.')

    @validates_schema
    def validate_bearer_format(self, data, **kwargs):
        if (data['type'] != 'http' or data['scheme'] != 'Bearer') and data.get('bearerFormat'):
            raise ValidationError(
                'Field <bearerFormat> applies to type <http> and scheme <Bearer>.'
            )
