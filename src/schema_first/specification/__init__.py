from copy import deepcopy
from pathlib import Path
from typing import Any

from marshmallow import fields
from marshmallow import INCLUDE
from marshmallow import RAISE
from marshmallow import Schema
from marshmallow import validate

from ..openapi import OpenAPI

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

        required_values = schema.get('enum')
        if required_values:
            validators.append(validate.OneOf(required_values))

        return validators

    def _convert_string_field(self, field_schema: dict, required: bool = False):
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
        initialized_schema.required = required
        return initialized_schema

    def _convert_boolean_field(self, field_schema: dict, required: bool = False):
        try:
            schema = FIELDS_VIA_TYPES[field_schema['type']]
        except KeyError:
            raise NotImplementedError(
                f'Schema <{field_schema}> for type <{field_schema["type"]}> not implemented.'
            )

        initialized_schema = schema()
        initialized_schema.allow_none = field_schema.get('nullable', False)
        initialized_schema.required = required
        return initialized_schema

    def _convert_field_any_type(self, field_schema: dict, required: bool = False):
        field_schema_converters = {
            'string': self._convert_string_field,
            'boolean': self._convert_boolean_field,
        }
        try:
            converted_field_schema = field_schema_converters[field_schema['type']](
                field_schema, required=required
            )
        except KeyError:
            raise NotImplementedError(
                f'Schema <{field_schema}> for type <{field_schema["type"]}> not be converted.'
            )

        return converted_field_schema

    def _convert_from_openapi_to_marshmallow_schema(self, open_api_schema: dict) -> type[Schema]:
        marshmallow_schema = {}
        for field_name, field_schema in open_api_schema['properties'].items():
            required_fields = open_api_schema.get('required', [])

            if field_name in required_fields:
                is_required = True
            else:
                is_required = False

            marshmallow_schema[field_name] = self._convert_field_any_type(
                field_schema, required=is_required
            )

        additionalProperties = open_api_schema.get('additionalProperties', True)
        if additionalProperties is False:
            marshmallow_schema['unknown'] = RAISE
        else:
            marshmallow_schema['unknown'] = INCLUDE

        return Schema.from_dict(marshmallow_schema)

    def _reassembly_of_schemas(self, obj: Any) -> Any:
        if isinstance(obj, dict):
            for k, v in obj.items():
                if k == 'schema':
                    obj[k] = self._convert_from_openapi_to_marshmallow_schema(v)
                else:
                    self._reassembly_of_schemas(v)

    def load(self) -> 'Specification':
        self.openapi.load()
        self.reassembly_spec = deepcopy(self.openapi.raw_spec)

        self._reassembly_of_schemas(self.reassembly_spec)

        return self
