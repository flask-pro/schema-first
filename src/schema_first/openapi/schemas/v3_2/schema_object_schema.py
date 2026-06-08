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

from schema_first.openapi.schemas.constants import FLOAT_FORMATS
from schema_first.openapi.schemas.constants import INT_FORMATS

from ..base import BaseSchema
from ..base import DocStringFields
from ..constants import FORMATS
from ..constants import TYPES


class BaseSchemaField(DocStringFields, BaseSchema):
    type = fields.String(required=True, validate=validate.OneOf(TYPES))
    nullable = fields.Boolean()

    @validates_schema
    def validate_default_via_format(self, data, **kwargs):
        if 'default' in data and 'format' in data:
            error = format_schemas[data['format']]().validate({'default': data['default']})
            if error:
                raise ValidationError(str(error))


class FormatBinarySchema(BaseSchema):
    default = fields.String()
    example = fields.String()


class FormatEmailSchema(BaseSchema):
    default = fields.Email()
    example = fields.Email()


class FormatDateSchema(BaseSchema):
    default = fields.Date()
    example = fields.Date()


class FormatDateTimeSchema(BaseSchema):
    default = fields.AwareDateTime(format='iso', default_timezone=None)
    example = fields.AwareDateTime(format='iso', default_timezone=None)


class FormatIPv4Schema(BaseSchema):
    default = fields.IPv4()
    example = fields.IPv4()


class FormatIPv6Schema(BaseSchema):
    default = fields.IPv6()
    example = fields.IPv6()


class FormatTimeSchema(BaseSchema):
    default = fields.Time(format='iso')
    example = fields.Time(format='iso')


class FormatURISchema(BaseSchema):
    default = fields.URL()
    example = fields.URL()


class FormatUUIDSchema(BaseSchema):
    default = fields.UUID()
    example = fields.UUID()


class FormatINT32Schema(BaseSchema):
    default = fields.Integer(validate=validate.Range(min=-2_147_483_648, max=2_147_483_647))
    example = fields.Integer(validate=validate.Range(min=-2_147_483_648, max=2_147_483_647))


class FormatINT64Schema(BaseSchema):
    default = fields.Integer(
        validate=validate.Range(min=-9_223_372_036_854_775_808, max=9_223_372_036_854_775_807)
    )
    example = fields.Integer(
        validate=validate.Range(min=-9_223_372_036_854_775_808, max=9_223_372_036_854_775_807)
    )


class FormatFloatSchema(BaseSchema):
    default = fields.Float(validate=validate.Range(min=3.4e-38, max=3.4e38))
    example = fields.Float(validate=validate.Range(min=3.4e-38, max=3.4e38))


class FormatDoubleSchema(BaseSchema):
    default = fields.Float(validate=validate.Range(min=1.7e-308, max=1.7e308))
    example = fields.Float(validate=validate.Range(min=1.7e-308, max=1.7e308))


class StringFieldSchema(BaseSchemaField):
    format = fields.String(validate=validate.OneOf(FORMATS))
    minLength = fields.Integer(validate=[validate.Range(min=0)])
    maxLength = fields.Integer(validate=[validate.Range(min=0)])
    enum = fields.List(fields.String())
    pattern = fields.String()
    default = fields.String()
    example = fields.String()

    @validates('pattern')
    def validate_pattern(self, value: str, data_key: str) -> None:
        try:
            re.compile(value)
        except re.PatternError as e:
            raise ValidationError(f"Pattern <{value}> is error <{repr(e)}>.")

    @validates_schema
    def validate_default_and_example(self, data, **kwargs):
        if 'default' in data:
            if 'pattern' in data:
                result = re.match(data['pattern'], data['default'])
                if result is None:
                    raise ValidationError(
                        f'<{data["default"]}> from default field does not match <{data["pattern"]}>'
                    )
            if 'enum' in data:
                if data['default'] not in data['enum']:
                    raise ValidationError(f'<{data["default"]}> not in <{data["enum"]}>')

        if 'example' in data:
            if 'pattern' in data:
                result = re.match(data['pattern'], data['example'])
                if result is None:
                    raise ValidationError(
                        f'<{data["example"]}> from example field does not match <{data["pattern"]}>'
                    )
            if 'enum' in data:
                if data['example'] not in data['enum']:
                    raise ValidationError(f'<{data["example"]}> not in <{data["enum"]}>')

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
    example = fields.Boolean(truthy=[True], falsy=[False])

    @validates_schema
    def validate_default(self, data, **kwargs):
        if 'default' in data:
            if not isinstance(data['default'], bool):
                raise ValidationError(f'<{data["default"]}> is not boolean.')


class NumberFieldSchema(BaseSchemaField):
    format = fields.String(validate=validate.OneOf(FLOAT_FORMATS))
    minimum = fields.Float()
    maximum = fields.Float()
    exclusiveMinimum = fields.Float()
    exclusiveMaximum = fields.Float()
    multipleOf = fields.Float(validate=[validate.Range(min=0, min_inclusive=False)])
    default = fields.Float()
    example = fields.Float()

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
    format = fields.String(validate=validate.OneOf(INT_FORMATS))
    minimum = fields.Integer()
    maximum = fields.Integer()
    exclusiveMinimum = fields.Integer()
    exclusiveMaximum = fields.Integer()
    multipleOf = fields.Integer(validate=[validate.Range(min=0, min_inclusive=False)])
    default = fields.Integer()
    example = fields.Integer()


field_schemas = {
    'boolean': BooleanFieldSchema,
    'integer': IntegerFieldSchema,
    'number': NumberFieldSchema,
    'object': ObjectFieldSchema,
    'string': StringFieldSchema,
}

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
    'int32': FormatINT32Schema,
    'int64': FormatINT64Schema,
    'float': FormatFloatSchema,
    'double': FormatDoubleSchema,
}


class SchemaObjectSchema(BaseSchemaField):
    type = fields.String(required=True, validate=validate.OneOf(TYPES))

    def load(
        self,
        data: Mapping[str, typing.Any] | Sequence[Mapping[str, typing.Any]],
        *,
        many: bool | None = None,
        partial: bool | types.StrSequenceOrSet | None = None,
        unknown: types.UnknownOption | None = None,
    ):
        if data['type'] == 'array':
            field_schema = ArrayFieldSchema
        else:
            try:
                field_schema = field_schemas[data['type']]
            except KeyError:
                raise ValidationError(f'Data type <{data["type"]}> not exist.')

        return field_schema().load(data, many=many, partial=partial, unknown=unknown)


class ArrayFieldSchema(BaseSchemaField):
    items = fields.Nested(SchemaObjectSchema, required=True)
    minItems = fields.Integer(validate=validate.Range(min=0))
    maxItems = fields.Integer(validate=validate.Range(min=0))
