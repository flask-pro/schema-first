import typing as t

from marshmallow import fields
from marshmallow import Schema
from marshmallow import ValidationError

from schema_first.query.exceptions import ContentTypeValidation
from schema_first.query.exceptions import CookiesValidation
from schema_first.query.exceptions import EndpointValidation
from schema_first.query.exceptions import HeadersValidation
from schema_first.query.exceptions import MethodParametersValidation
from schema_first.query.exceptions import MethodValidation
from schema_first.query.exceptions import PathParametersValidation
from schema_first.query.exceptions import QueryParametersValidation
from schema_first.query.exceptions import RequestValidation
from schema_first.query.exceptions import ResponseValidation
from schema_first.query.exceptions import StatusCodeValidation
from schema_first.specification import Specification


class HTTPQueryValidator:
    def __init__(self, spec: Specification) -> None:
        self.spec = spec

        self.request_fields = {}
        self.response_fields = {}

    def _get_method_data(self, **data: dict[str, t.Any]) -> dict:
        endpoint = self.spec.reassembly_spec['paths'].get(data['endpoint'])
        if not endpoint:
            raise EndpointValidation(f'Path <{data['endpoint']}> not in OpenAPI specification.')

        method = endpoint.get(data['method'])
        if not method:
            raise MethodValidation(f'Method <{data['method']}> not in OpenAPI specification.')

        return method

    def _make_schema_for_request(self, **data: dict[str, t.Any]) -> type[Schema]:
        method_data = self._get_method_data(**data)

        self.request_fields['endpoint'] = fields.String()
        self.request_fields['method'] = fields.String()

        if 'body' in data:
            content_type = method_data['requestBody']['content'].get(data['content_type'])
            if not content_type:
                raise ContentTypeValidation(
                    f'Content type <{data['content_type']}> not in OpenAPI specification.'
                )

            self.request_fields['content_type'] = fields.String()
            self.request_fields['body'] = fields.Nested(content_type['schema'])

        if 'path_params' in data or 'query_params' in data or 'headers' in data:
            try:
                parameters = method_data['parameters']
            except KeyError as exc:
                raise MethodParametersValidation(
                    f'Parameters <{data['path_params']}> not in OpenAPI specification.'
                ) from exc

            if 'path_params' in data:
                try:
                    path_params = parameters['paths']
                except KeyError as exc:
                    raise PathParametersValidation(
                        f'Path parameters <{data['path_params']}> not in OpenAPI specification.'
                    ) from exc

                self.request_fields['path_params'] = fields.Nested(path_params['schema'])

            if 'query_params' in data:
                try:
                    query_params = parameters['queries']
                except KeyError as exc:
                    raise QueryParametersValidation(
                        f'Query parameters <{data['query_params']}> not in OpenAPI specification.'
                    ) from exc

                self.request_fields['query_params'] = fields.Nested(query_params['schema'])

            if 'headers' in data:
                try:
                    headers = parameters['headers']
                except KeyError as exc:
                    raise HeadersValidation(
                        f'Headers <{data['headers']}> not in OpenAPI specification.'
                    ) from exc

                self.request_fields['headers'] = fields.Nested(headers['schema'])

            if 'cookies' in data:
                try:
                    cookies = parameters['cookies']
                except KeyError as exc:
                    raise CookiesValidation(
                        f'Cookies <{data['cookies']}> not in OpenAPI specification.'
                    ) from exc

                self.request_fields['cookies'] = fields.Nested(cookies['schema'])

        return Schema.from_dict(self.request_fields)

    def _make_schema_for_response(self, **data: dict[str, t.Any]) -> type[Schema]:
        method_data = self._get_method_data(**data)

        self.response_fields['endpoint'] = fields.String()
        self.response_fields['method'] = fields.String()

        status_code = method_data['responses'].get(data['status_code'])
        if not status_code:
            raise StatusCodeValidation(
                f'Status code <{data['status_code']}> not in OpenAPI specification.'
            )

        self.response_fields['status_code'] = fields.String()

        content_type = status_code['content'].get(data['content_type'])
        if not content_type:
            raise ContentTypeValidation(
                f'Content type <{data['content_type']}> not in OpenAPI specification.'
            )

        self.response_fields['content_type'] = fields.String()
        self.response_fields['body'] = fields.Nested(content_type['schema'])

        return Schema.from_dict(self.response_fields)

    def request_handler(
        self,
        endpoint: str,
        method: t.Literal['post', 'get', 'update', 'patch', 'delete'],
        content_type: t.Literal['application/json'],
        headers: dict[str, t.Any] or ... = ...,
        cookies: dict[str, t.Any] or ... = ...,
        body: dict[str, t.Any] or ... = ...,
        path_params: dict[str, t.Any] or ... = ...,
        query_params: dict[str, t.Any] or ... = ...,
    ):
        all_kwargs = {
            'endpoint': endpoint,
            'method': method,
            'content_type': content_type,
            'headers': headers,
            'cookies': cookies,
            'body': body,
            'path_params': path_params,
            'query_params': query_params,
        }
        data = {k: v for k, v in all_kwargs.items() if v is not ...}

        schema = self._make_schema_for_request(**data)

        try:
            deserialized_data = schema().load(data)
        except ValidationError as exc:
            raise RequestValidation(
                f'For query <{data}> validation error <{exc.args[0]}>.'
            ) from exc

        return deserialized_data

    def response_handler(
        self,
        endpoint: str,
        method: t.Literal['post', 'get', 'update', 'patch', 'delete'],
        content_type: t.Literal['application/json'],
        status_code: str,
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
            raise ResponseValidation(f'Response <{data} validation error>') from exc

        return deserialized_data
