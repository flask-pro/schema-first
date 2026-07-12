import json
from typing import Any
import typing as t


class ConverterOpenAPIToSpilliAPI:
    def __init__(self, open_api_spec: dict) -> None:
        self.open_api_spec = open_api_spec
        self.spilli_api_spec = None

    def _convert_params_to_schema(
        self, params: list[dict], place: t.Literal['header', 'cookie', 'path', 'query']
    ) -> Any | None:
        schema = {
            'type': 'object',
            'additionalProperties': True,
        }

        required = []
        properties = {}
        for param in params:
            if param['in'] == place:
                if param.get('required', False):
                    required.append(param['name'])
                properties[param['name']] = param['schema']

        if not properties:
            return None
        else:
            schema['properties'] = properties

        if required:
            schema['required'] = required

        return schema

    def _params_list_to_dict(self, params: list[dict]) -> dict:
        params_as_dict = {}
        if headers := self._convert_params_to_schema(params, 'header'):
            params_as_dict['headers'] = {'schema': headers}
        if cookies := self._convert_params_to_schema(params, 'cookie'):
            params_as_dict['cookies'] = {'schema': cookies}
        if paths := self._convert_params_to_schema(params, 'path'):
            params_as_dict['paths'] = {'schema': paths}
        if queries := self._convert_params_to_schema(params, 'query'):
            params_as_dict['queries'] = {'schema': queries}

        return params_as_dict

    def _make_to_spilli_api_format(self) -> None:
        self.spilli_api_spec = json.loads(json.dumps(self.open_api_spec))

        for _, methods in self.spilli_api_spec['paths'].items():
            common_params = []
            if 'parameters' in methods:
                common_params = methods.pop('parameters', [])

            for _, operation_obj in methods.items():
                if 'parameters' in operation_obj:
                    method_params = common_params + operation_obj.pop('parameters', [])
                    operation_obj['parameters'] = self._params_list_to_dict(method_params)

    def convert(self) -> dict:
        self._make_to_spilli_api_format()
        return self.spilli_api_spec
