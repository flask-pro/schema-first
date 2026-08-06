from pathlib import Path

import pytest

from tests.conftest import openapi_3_2_path_specs


@pytest.mark.parametrize(
    'file_path',
    [
        Path(openapi_3_2_path_specs, 'schemas', 'all_of.yaml'),
        Path(openapi_3_2_path_specs, 'schemas', 'any_of.yaml'),
        Path(openapi_3_2_path_specs, 'schemas', 'one_of.yaml'),
    ],
)
def test_schema_object__multi_schemas(fx_open_spec, file_path):

    with pytest.raises(NotImplementedError):
        fx_open_spec(file_path)
