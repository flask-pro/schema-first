from pathlib import Path
from typing import Any

from marshmallow import fields
from marshmallow import INCLUDE
from marshmallow import RAISE
from marshmallow import Schema
from marshmallow import validate
from marshmallow.fields import Field

from schema_first.openapi import OpenAPI
from schema_first.specification.spilli_api import ConverterOpenAPIToSpilliAPI

FIELDS_VIA_TYPES = {
    'boolean': fields.Boolean,
    'number': fields.Float,
    'string': fields.String,
    'integer': fields.Integer,
}

FIELDS_VIA_FORMATS = {
    'uuid': fields.UUID,
    'date-time': fields.AwareDateTime,
    'date': fields.Date,
    'time': fields.Time,
    'email': fields.Email,
    'ipv4': fields.IPv4,
    'ipv6': fields.IPv6,
    'uri': fields.Url,
    'binary': fields.String,
    'string': fields.String,
}


class Specification:
    def __init__(self, spec_file: Path | str):
        self.openapi = OpenAPI(spec_file)
        self.spilli_api = None
        self.reassembly_spec = None

    @staticmethod
    def _make_field_validators(schema: dict) -> list[validate.Validator]:
        validators = []

        if schema['type'] in ['string']:
            validators.append(
                validate.Length(min=schema.get('minLength'), max=schema.get('maxLength'))
            )
            if schema.get('pattern'):
                validators.append(validate.Regexp(schema['pattern']))

        if schema['type'] in ['integer', 'number']:
            validators.append(validate.Range(min=schema.get('minimum'), max=schema.get('maximum')))

        if required_values := schema.get('enum'):
            validators.append(validate.OneOf(required_values))

        return validators

    def _convert_string_field(self, field_schema: dict):
        format_string = field_schema.get('format', 'string')
        try:
            schema = FIELDS_VIA_FORMATS[format_string]
        except KeyError:
            raise NotImplementedError(
                f'Schema <{field_schema}> for format <{format_string}> not implemented.'
            )

        initialized_schema = schema()
        initialized_schema.validate = self._make_field_validators(field_schema)
        initialized_schema.allow_none = field_schema.get('nullable', False)
        initialized_schema.required = field_schema.get('required', False)
        return initialized_schema

    def _convert_boolean_field(self, field_schema: dict):
        try:
            schema = FIELDS_VIA_TYPES[field_schema['type']]
        except KeyError:
            raise NotImplementedError(
                f'Schema <{field_schema}> for type <{field_schema["type"]}> not implemented.'
            )

        initialized_schema = schema()
        initialized_schema.allow_none = field_schema.get('nullable', False)
        initialized_schema.required = field_schema.get('required', False)
        return initialized_schema

    def _convert_number_field(self, field_schema: dict):
        try:
            schema = FIELDS_VIA_TYPES[field_schema['type']]
        except KeyError:
            raise NotImplementedError(
                f'Schema <{field_schema}> for type <{field_schema["type"]}> not implemented.'
            )

        initialized_schema = schema()
        initialized_schema.validate = self._make_field_validators(field_schema)
        initialized_schema.allow_none = field_schema.get('nullable', False)
        initialized_schema.required = field_schema.get('required', False)
        return initialized_schema

    def _convert_field_any_type(self, field_schema: dict):
        field_schema_converters = {
            'string': self._convert_string_field,
            'boolean': self._convert_boolean_field,
            'number': self._convert_number_field,
            'integer': self._convert_number_field,
            'object': self._convert_object_field,
            'array': self._convert_array_field,
        }
        try:
            converted_field_schema = field_schema_converters[field_schema['type']](field_schema)
        except KeyError:
            raise NotImplementedError(
                f'Schema <{field_schema}> for type <{field_schema["type"]}> not be converted.'
            )

        return converted_field_schema

    def _convert_object_field(self, open_api_schema: dict) -> type[Schema]:
        marshmallow_schema = {}
        required_fields = open_api_schema.get('required', [])
        for field_name, field_schema in open_api_schema['properties'].items():
            if field_name in required_fields and field_schema['type'] != 'object':
                field_schema['required'] = True

            marshmallow_schema[field_name] = self._convert_field_any_type(field_schema)

        additionalProperties = open_api_schema.get('additionalProperties', True)
        if additionalProperties is False:
            marshmallow_schema['unknown'] = RAISE
        else:
            marshmallow_schema['unknown'] = INCLUDE

        return Schema.from_dict(marshmallow_schema)

    def _convert_array_field(self, open_api_schema: dict) -> Field:
        array_item_schema = open_api_schema['items']
        if array_item_schema['type'] == 'object':
            nested_field = self._convert_object_field(array_item_schema)
            array_field = fields.Nested(nested_field, many=True)
        else:
            nested_field = FIELDS_VIA_TYPES[array_item_schema['type']]()
            array_field = fields.List(nested_field)
        return array_field

    def _reassembly_of_schemas(self, obj: Any) -> None:
        if isinstance(obj, dict):
            for k, v in obj.items():
                # Checking for object type is needed to skip already resolved schemes.
                # This is necessary because of passing variables by reference in Python.
                if k == 'schema' and isinstance(v, dict):
                    obj[k] = self._convert_field_any_type(v)
                else:
                    self._reassembly_of_schemas(v)

    def load(self) -> Specification:
        self.openapi.load()

        self.reassembly_spec = ConverterOpenAPIToSpilliAPI(self.openapi.raw_spec).convert()
        self._reassembly_of_schemas(self.reassembly_spec)

        return self
