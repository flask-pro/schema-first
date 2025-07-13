from pathlib import Path

import pytest
import yaml
from openapi_spec_validator import validate as osv_validate
from openapi_spec_validator.readers import read_from_filename

pytest_plugins = (
    'tests.schemas.info_object.conftest',
    'tests.schemas.contact_object.conftest',
    'tests.schemas.license_object.conftest',
    'tests.schemas.server_object.conftest',
)


@pytest.fixture
def fx_spec_minimal(fx_info_object_minimal):
    payload = {
        'openapi': '3.1.1',
        'info': fx_info_object_minimal,
        'paths': {
            '/endpoint': {
                'get': {
                    'operationId': 'endpoint',
                    'responses': {
                        '200': {
                            'description': 'OK',
                            'content': {
                                'application/json': {
                                    'schema': {
                                        'type': 'object',
                                        'properties': {'message': {'type': 'string'}},
                                    }
                                }
                            },
                        }
                    },
                }
            }
        },
    }
    return payload


@pytest.fixture
def fx_spec_full(fx_info_object_full, fx_server_object_full):
    payload = {
        'openapi': '3.1.1',
        'info': fx_info_object_full,
        'jsonSchemaDialect': 'https://json-schema.org/draft/2020-12/schema',
        'servers': [fx_server_object_full],
        'paths': {
            '/endpoint': {
                'get': {
                    'operationId': 'endpoint',
                    'responses': {
                        '200': {
                            'description': 'OK',
                            'content': {
                                'application/json': {
                                    'schema': {
                                        'type': 'object',
                                        'properties': {'message': {'type': 'string'}},
                                    }
                                }
                            },
                        }
                    },
                }
            }
        },
    }
    return payload


@pytest.fixture
def fx_spec_as_file(tmp_path):
    def create(
        spec: dict, external_validator: bool = False, file_name: str = 'openapi.yaml'
    ) -> Path:
        spec_path = Path(tmp_path, file_name)
        with open(spec_path, 'w+') as f:
            yaml.dump(spec, f)

        spec_as_dict, _ = read_from_filename(str(spec_path))
        if external_validator:
            osv_validate(spec_as_dict)

        return spec_path

    return create
