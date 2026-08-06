import typing as t

from marshmallow import fields
from marshmallow import Schema

from schema_first.query.exceptions import ContentTypeValidation
from schema_first.query.exceptions import EndpointValidation
from schema_first.query.exceptions import MethodParametersValidation
from schema_first.query.exceptions import MethodValidation
from schema_first.query.exceptions import PathParametersValidation
from schema_first.query.exceptions import QueryParametersValidation
from schema_first.query.exceptions import StatusCodeValidation
from schema_first.specification import Specification


class Request(t.TypedDict):
    endpoint: str
    method: t.Literal['post', 'get', 'update', 'patch', 'delete']
    content_type: t.Literal['application/json']
    body: dict[str, t.Any] | None


class HTTPQueryValidator:
    def __init__(self, spec: Specification) -> None:
        self.spec = spec

    def _get_method_data(self, **data: Request) -> dict:
        endpoint = self.spec.reassembly_spec['paths'].get(data['endpoint'])
        if not endpoint:
            raise EndpointValidation(f'Path <{data['endpoint']}> not in OpenAPI specification.')

        method = endpoint.get(data['method'])
        if not method:
            raise MethodValidation(f'Method <{data['method']}> not in OpenAPI specification.')

        return method

    def _make_schema_for_request(self, **data: Request) -> type[Schema]:
        schema_as_dict = {}

        method_data = self._get_method_data(**data)

        schema_as_dict['endpoint'] = fields.String()
        schema_as_dict['method'] = fields.String()

        if 'body' in data:
            content_type = method_data['requestBody']['content'].get(data['content_type'])
            if not content_type:
                raise ContentTypeValidation(
                    f'Content type <{data['content_type']}> not in OpenAPI specification.'
                )

            schema_as_dict['content_type'] = fields.String()
            schema_as_dict['body'] = fields.Nested(content_type['schema'])

        if 'path_params' in data or 'query_params' in data:
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

                schema_as_dict['path_params'] = fields.Nested(path_params['schema'])

            if 'query_params' in data:
                try:
                    query_params = parameters['queries']
                except KeyError as exc:
                    raise QueryParametersValidation(
                        f'Query parameters <{data['query_params']}> not in OpenAPI specification.'
                    ) from exc

                schema_as_dict['query_params'] = fields.Nested(query_params['schema'])

        return Schema.from_dict(schema_as_dict)

    def _make_schema_for_response(self, **data: Request) -> type[Schema]:
        schema_as_dict = {}

        method_data = self._get_method_data(**data)

        schema_as_dict['endpoint'] = fields.String()
        schema_as_dict['method'] = fields.String()

        status_code = method_data['responses'].get(data['status_code'])
        if not status_code:
            raise StatusCodeValidation(
                f'Status code <{data['status_code']}> not in OpenAPI specification.'
            )

        schema_as_dict['status_code'] = fields.String()

        content_type = status_code['content'].get(data['content_type'])
        if not content_type:
            raise ContentTypeValidation(
                f'Content type <{data['content_type']}> not in OpenAPI specification.'
            )

        schema_as_dict['content_type'] = fields.String()
        schema_as_dict['body'] = fields.Nested(content_type['schema'])

        return Schema.from_dict(schema_as_dict)

    def request_handler(self, **data: Request):
        schema = self._make_schema_for_request(**data)
        deserialized_data = schema().load(data)

        return deserialized_data

    def response_handler(self, **data: Request):
        schema = self._make_schema_for_response(**data)
        deserialized_data = schema().load(data)

        return deserialized_data
