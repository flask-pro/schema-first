import re

from marshmallow import fields
from marshmallow import RAISE
from marshmallow import Schema
from marshmallow import validate
from marshmallow import validates
from marshmallow import validates_schema
from marshmallow import ValidationError

from ..base import BaseSchema
from ..constants import FORMATS
from ..constants import TYPES
from ..fields import DESCRIPTION_FIELD


class FormatBinarySchema(Schema):
    class Meta:
        unknown = RAISE

    default = fields.String()


class FormatEmailSchema(Schema):
    class Meta:
        unknown = RAISE

    default = fields.Email()


class FormatDateSchema(Schema):
    class Meta:
        unknown = RAISE

    default = fields.Date()


class FormatDateTimeSchema(Schema):
    class Meta:
        unknown = RAISE

    default = fields.AwareDateTime(format='iso', default_timezone=None)


class FormatIPv4Schema(Schema):
    class Meta:
        unknown = RAISE

    default = fields.IPv4()


class FormatIPv6Schema(Schema):
    class Meta:
        unknown = RAISE

    default = fields.IPv6()


class FormatTimeSchema(Schema):
    class Meta:
        unknown = RAISE

    default = fields.Time(format='iso')


class FormatURISchema(Schema):
    class Meta:
        unknown = RAISE

    default = fields.URL()


class FormatUUIDSchema(Schema):
    class Meta:
        unknown = RAISE

    default = fields.UUID()


format_schemas = {
    'binary': FormatBinarySchema,
    'date': FormatDateSchema,
    'date-time': FormatDateTimeSchema,
    'email': FormatEmailSchema,
    'ipv4': FormatIPv4Schema,
    'ipv6': FormatIPv6Schema,
    'time': FormatTimeSchema,
    'uri': FormatURISchema,
    'uuid': FormatUUIDSchema,
}


class StringFieldSchema(BaseSchema):
    format = fields.String(validate=validate.OneOf(FORMATS))
    minLength = fields.Integer(validate=[validate.Range(min=0)])
    maxLength = fields.Integer(validate=[validate.Range(min=0)])
    pattern = fields.String()

    @validates('pattern')
    def validate_pattern(self, value: str, data_key: str) -> None:
        try:
            re.compile(value)
        except re.PatternError as e:
            raise ValidationError(f"Pattern <{value}> is error <{repr(e)}>.")

    @validates_schema
    def validate_default(self, data, **kwargs):
        if 'default' in data and 'pattern' in data:
            result = re.match(data['pattern'], data['default'])
            if result is None:
                raise ValidationError(f'<{data["default"]}> does not match <{data["pattern"]}>')

    @validates_schema
    def validate_default_via_format(self, data, **kwargs):
        if 'default' in data and 'format' in data:
            error = format_schemas[data['format']]().validate({'default': data['default']})
            if error:
                raise ValidationError(str(error))

    @validates_schema
    def validate_length(self, data, **kwargs):
        if 'minLength' in data and 'maxLength' in data:
            if data['minLength'] > data['maxLength']:
                raise ValidationError(
                    f'<{data['minLength']}> cannot be greater than <{data['maxLength']}>'
                )


class SchemaObjectSchema(StringFieldSchema):
    type = fields.String(required=True, validate=validate.OneOf(TYPES))
    default = fields.String()
    description = DESCRIPTION_FIELD
    nullable = fields.Boolean()
    required = fields.List(fields.String())
    additionalProperties = fields.Boolean()

    properties = fields.Dict(
        keys=fields.String(required=True, validate=validate.Length(min=1)),
        values=fields.Nested(lambda: SchemaObjectSchema()),
    )

    @validates_schema
    def validate_required(self, data, **kwargs):
        if 'required' in data:
            for field_name in data['required']:
                if field_name not in data['properties']:
                    raise ValidationError(
                        f'Required field <{field_name}> not in <data["properties"]>'
                    )
