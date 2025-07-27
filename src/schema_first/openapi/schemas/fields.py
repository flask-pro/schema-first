from marshmallow import fields
from marshmallow import validate

ENDPOINT_FIELD = fields.String(required=True, validate=validate.Regexp(r'^[/][0-9a-z-{}/]*[^/]$'))
HTTP_CODE_FIELD = fields.String(required=True, validate=validate.Regexp(r'^[1-5]{1}\d{2}|default$'))
SUMMARY_FIELD = fields.String()
DESCRIPTION_FIELD = fields.String()
REQUIRED_DESCRIPTION_FIELD = fields.String(required=True)
MEDIA_TYPE_FIELD = fields.String(required=True)
REF_FIELD = fields.String(
    required=True, data_key='$ref', validate=validate.Regexp(r'^#/[a-zA-Z/]*$')
)
