from pathlib import Path

from openapi_spec_validator import validate as osv_validate
from openapi_spec_validator.readers import read_from_filename
import pytest
import yaml

pytest_plugins = (
    'tests.objects.info_object.conftest',
    'tests.objects.contact_object.conftest',
    'tests.objects.license_object.conftest',
    'tests.objects.schema_object.conftest',
    'tests.objects.schema_object.string_field.conftest',
    'tests.objects.server_object.conftest',
)


@pytest.fixture
def fx_spec_required(fx_info_object_required, fx_schema_object__required):
    payload = {
        'openapi': '3.1.1',
        'info': fx_info_object_required,
        'paths': {
            '/endpoint': {
                'get': {
                    'operationId': 'endpoint-get',
                    'responses': {
                        '200': {
                            'description': 'OK',
                            'content': {'application/json': {'schema': fx_schema_object__required}},
                        }
                    },
                }
            }
        },
    }
    return payload


@pytest.fixture
def fx_spec_full(fx_info_object_full, fx_server_object_full, fx_schema_object__full):
    payload = {
        'openapi': '3.1.1',
        'info': fx_info_object_full,
        'jsonSchemaDialect': 'https://json-schema.org/draft/2020-12/schema',
        'servers': [fx_server_object_full],
        'paths': {
            '/endpoint': {
                'get': {
                    'operationId': 'endpoint-get',
                    'responses': {
                        '200': {
                            'description': 'OK',
                            'content': {'application/json': {'schema': fx_schema_object__full}},
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
