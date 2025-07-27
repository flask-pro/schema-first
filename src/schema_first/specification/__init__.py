from copy import deepcopy
from pathlib import Path
from typing import Any

from marshmallow import fields
from marshmallow import Schema

from ..openapi import OpenAPI

FIELDS_VIA_TYPES = {
    'boolean': fields.Boolean,
    'number': fields.Float,
    'string': fields.String,
    'integer': fields.Integer,
}


class Specification:
    def __init__(self, spec_file: Path | str):
        self.openapi = OpenAPI(spec_file)
        self.reassembly_spec = None

    def _convert_from_openapi_to_marshmallow_schema(self, open_api_schema: dict) -> type[Schema]:
        if open_api_schema['type'] == 'object':
            marshmallow_schema = {}
            for field_name, field in open_api_schema['properties'].items():
                marshmallow_schema[field_name] = FIELDS_VIA_TYPES[field['type']]()
        else:
            raise NotImplementedError(open_api_schema)

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
