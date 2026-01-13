from collections.abc import Mapping, Sequence
import math
import re
import typing

from marshmallow import fields
from marshmallow import types
from marshmallow import validate
from marshmallow import validates
from marshmallow import validates_schema
from marshmallow import ValidationError

from ..base import BaseSchema
from ..constants import FORMATS
from ..constants import TYPES
from ..fields import DESCRIPTION_FIELD


class BaseSchemaField(BaseSchema):
    type = fields.String(required=True, validate=validate.OneOf(TYPES))
    description = DESCRIPTION_FIELD
    nullable = fields.Boolean()


class FormatBinarySchema(BaseSchema):
    default = fields.String()


class FormatEmailSchema(BaseSchema):
    default = fields.Email()


class FormatDateSchema(BaseSchema):
    default = fields.Date()


class FormatDateTimeSchema(BaseSchema):
    default = fields.AwareDateTime(format='iso', default_timezone=None)


class FormatIPv4Schema(BaseSchema):
    default = fields.IPv4()


class FormatIPv6Schema(BaseSchema):
    default = fields.IPv6()


class FormatTimeSchema(BaseSchema):
    default = fields.Time(format='iso')


class FormatURISchema(BaseSchema):
    default = fields.URL()


class FormatUUIDSchema(BaseSchema):
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


class StringFieldSchema(BaseSchemaField):
    format = fields.String(validate=validate.OneOf(FORMATS))
    minLength = fields.Integer(validate=[validate.Range(min=0)])
    maxLength = fields.Integer(validate=[validate.Range(min=0)])
    pattern = fields.String()
    default = fields.String()

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
                    f'<{data["minLength"]}> cannot be greater than <{data["maxLength"]}>'
                )


class ObjectFieldSchema(BaseSchemaField):
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


class BooleanFieldSchema(BaseSchemaField):
    default = fields.Boolean(truthy=[True], falsy=[False])

    @validates_schema
    def validate_default(self, data, **kwargs):
        if 'default' in data:
            if not isinstance(data['default'], bool):
                raise ValidationError(f'<{data["default"]}> is not boolean.')


class NumberFieldSchema(BaseSchemaField):
    minimum = fields.Float()
    maximum = fields.Float()
    exclusiveMinimum = fields.Float()
    exclusiveMaximum = fields.Float()
    multipleOf = fields.Float(validate=[validate.Range(min=0, min_inclusive=False)])
    default = fields.Float()

    @validates_schema
    def validate_default(self, data, **kwargs):
        if 'default' in data:
            default = data['default']

            minimum = data.get('minimum', -math.inf)
            maximum = data.get('maximum', math.inf)
            if not minimum <= default <= maximum:
                raise ValidationError(
                    f'Value <{default}> must be greater than or equal to <{minimum}>'
                    f' and less than or equal to <{maximum}>.'
                )

            exclusive_minimum = data.get('exclusiveMinimum', -math.inf)
            exclusive_maximum = data.get('exclusiveMaximum', math.inf)
            if not exclusive_minimum < default < exclusive_maximum:
                raise ValidationError(
                    f'Value <{default}> must be greater to <{minimum}> and less to <{maximum}>.'
                )

    @validates_schema
    def validate_min_max(self, data, **kwargs):
        if 'exclusiveMinimum' in data and 'exclusiveMaximum' in data:
            exclusive_min = data['exclusiveMinimum']
            exclusive_max = data['exclusiveMaximum']
            if exclusive_min > exclusive_max:
                raise ValidationError(f'<{exclusive_min}> cannot be greater than <{exclusive_max}>')

        if 'minimum' in data and 'maximum' in data:
            minimum = data['minimum']
            maximum = data['maximum']
            if minimum > maximum:
                raise ValidationError(f'<{minimum}> cannot be greater than <{maximum}>')


class IntegerFieldSchema(NumberFieldSchema):
    minimum = fields.Integer()
    maximum = fields.Integer()
    exclusiveMinimum = fields.Integer()
    exclusiveMaximum = fields.Integer()
    multipleOf = fields.Integer(validate=[validate.Range(min=0, min_inclusive=False)])
    default = fields.Integer()


field_schemas = {
    'boolean': BooleanFieldSchema,
    'object': ObjectFieldSchema,
    'string': StringFieldSchema,
    'number': NumberFieldSchema,
    'integer': IntegerFieldSchema,
}


class SchemaObjectSchema(BaseSchema):
    type = fields.String(required=True, validate=validate.OneOf(TYPES))

    def load(
        self,
        data: Mapping[str, typing.Any] | Sequence[Mapping[str, typing.Any]],
        *,
        many: bool | None = None,
        partial: bool | types.StrSequenceOrSet | None = None,
        unknown: types.UnknownOption | None = None,
    ):
        try:
            return field_schemas[data['type']]().load(
                data, many=many, partial=partial, unknown=unknown
            )
        except KeyError:
            raise ValidationError(f'Data type <{data["type"]}> not supported.')
