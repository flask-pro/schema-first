from marshmallow import Schema


def get_schema_from_request(spec: dict, endpoint: str, status_code: str) -> type[Schema]:
    return spec['paths'][endpoint]['get']['responses'][status_code]['content']['application/json'][
        'schema'
    ]
