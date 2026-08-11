import typing as t

from marshmallow import fields
from marshmallow import INCLUDE
from marshmallow import Schema
from marshmallow import ValidationError

from schema_first.query.exceptions import EndpointValidation
from schema_first.query.exceptions import MethodValidation
from schema_first.query.exceptions import RequestValidation
from schema_first.query.exceptions import ResponseValidation
from schema_first.specification import Specification


class HTTPQueryValidator:
    def __init__(self, spec: Specification) -> None:
        self.spec = spec

    def _get_method_data(self, **data: dict[str, t.Any]) -> dict:
        endpoint = self.spec.reassembly_spec['paths'].get(data['endpoint'])
        if not endpoint:
            raise EndpointValidation(f'Path <{data['endpoint']}> not in OpenAPI specification.')

        method_data = endpoint.get(data['method'])
        if not method_data:
            raise MethodValidation(f'Method <{data['method']}> not in OpenAPI specification.')

        return method_data

    def _make_schema_for_request(self, **data: dict[str, t.Any]) -> type[Schema]:
        method_data = self._get_method_data(**data)

        request_fields = {'endpoint': fields.String(), 'method': fields.String()}

        if request_body := method_data.get('requestBody'):
            content = request_body.get('content')
            if content:
                content_type = content.get(data.get('content_type'))
                if content_type:
                    request_fields['content_type'] = fields.String()

                    body_schema = content_type.get('schema')
                    if body_schema:
                        request_fields['body'] = fields.Nested(body_schema)

        if parameters := method_data.get('parameters'):
            for name_params, schema in parameters.items():
                params_schema = schema.get('schema')

                if not params_schema:
                    continue

                if name_params == 'headers':
                    request_fields[name_params] = fields.Nested(params_schema, unknown=INCLUDE)
                else:
                    request_fields[name_params] = fields.Nested(params_schema)

                if 'headers' not in parameters:
                    request_fields['headers'] = fields.Raw()

        if not parameters:
            request_fields['headers'] = fields.Raw()

        request_schema = Schema.from_dict(request_fields)

        return request_schema

    def _make_schema_for_response(self, **data: dict[str, t.Any]) -> type[Schema]:
        method_data = self._get_method_data(**data)

        response_fields = {'endpoint': fields.String(), 'method': fields.String()}

        status_code = method_data['responses'].get(data['status_code'])
        if not status_code:
            status_code = method_data['responses'].get('default')

        if status_code:
            response_fields['status_code'] = fields.String()

        if content := status_code.get('content'):
            content_type = content.get(data['content_type'])
            if content_type:
                response_fields['content_type'] = fields.String()

                body_schema = content_type.get('schema')
                if body_schema:
                    response_fields['body'] = fields.Nested(body_schema)
            elif 'application/octet-stream' in content:
                response_fields['content_type'] = fields.String()
                response_fields['body'] = fields.Raw()
            else:
                raise NotImplementedError

        else:
            # If body must be empty.
            if data.get('content_type'):
                response_fields['content_type'] = fields.String()

        response_schema = Schema.from_dict(response_fields)
        response_schema.Meta.unknown = 'raise'

        return response_schema

    def request_handler(
        self,
        endpoint: str,
        method: t.Literal['post', 'get', 'update', 'patch', 'delete'],
        content_type: t.Literal['application/json'] or ... = ...,
        headers: dict[str, t.Any] or ... = ...,
        cookies: dict[str, t.Any] or ... = ...,
        body: dict[str, t.Any] or ... = ...,
        paths: dict[str, t.Any] or ... = ...,
        queries: dict[str, t.Any] or ... = ...,
    ):
        all_kwargs = {
            'endpoint': endpoint,
            'method': method,
            'content_type': content_type,
            'headers': headers,
            'cookies': cookies,
            'body': body,
            'paths': paths,
            'queries': queries,
        }
        data = {k: v for k, v in all_kwargs.items() if v is not ...}

        schema = self._make_schema_for_request(**data)

        try:
            deserialized_data = schema().load(data)
        except ValidationError as exc:
            raise RequestValidation(f'Request <{data}> validation error <{exc.args}>.') from exc

        return deserialized_data

    def response_handler(
        self,
        endpoint: str,
        method: t.Literal['post', 'get', 'update', 'patch', 'delete'],
        status_code: str,
        content_type: str or ... = ...,
        body: dict[str, t.Any] or ... = ...,
    ):
        all_kwargs = {
            'endpoint': endpoint,
            'method': method,
            'content_type': content_type,
            'status_code': status_code,
            'body': body,
        }
        data = {k: v for k, v in all_kwargs.items() if v is not ...}
        schema = self._make_schema_for_response(**data)

        try:
            deserialized_data = schema().load(data)
        except ValidationError as exc:
            raise ResponseValidation(f'Response <{data}> validation error <{exc.args}>.') from exc

        return deserialized_data
