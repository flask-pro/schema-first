import os
from pathlib import Path

from openapi_spec_validator import validate as osv_validate
from openapi_spec_validator.readers import read_from_filename
import pytest
import yaml

tests_dir_abspath = os.path.dirname(os.path.abspath(__file__))

pytest_plugins = (
    'tests.objects.contact_object.conftest',
    'tests.objects.example_object.conftest',
    'tests.objects.external_docs_object.conftest',
    'tests.objects.info_object.conftest',
    'tests.objects.license_object.conftest',
    'tests.objects.media_type_object.conftest',
    'tests.objects.openapi_object.conftest',
    'tests.objects.operation_object.conftest',
    'tests.objects.path_item_object.conftest',
    'tests.objects.paths_object.conftest',
    'tests.objects.response_object.conftest',
    'tests.objects.responses_object.conftest',
    'tests.objects.schema_object.conftest',
    'tests.objects.schema_object.string_field.conftest',
    'tests.objects.schema_object.boolean_field.conftest',
    'tests.objects.schema_object.number_field.conftest',
    'tests.objects.schema_object.integer_field.conftest',
    'tests.objects.server_object.conftest',
    'tests.objects.tag_object.conftest',
)


@pytest.fixture
def fx_spec_required(fx_openapi_object__required):
    return fx_openapi_object__required


@pytest.fixture
def fx_spec_full(fx_openapi_object_full):
    return fx_openapi_object_full


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
