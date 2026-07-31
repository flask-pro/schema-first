from pathlib import Path

import pytest

from tests.conftest import tests_dir_abspath


@pytest.mark.parametrize(
    'file_path',
    [
        Path(tests_dir_abspath, '_contrib', 'specs', 'v3.2', 'schemas', 'all_of.yaml'),
        Path(tests_dir_abspath, '_contrib', 'specs', 'v3.2', 'schemas', 'any_of.yaml'),
        Path(tests_dir_abspath, '_contrib', 'specs', 'v3.2', 'schemas', 'one_of.yaml'),
    ],
)
def test_schema_object__multi_schemas(fx_open_spec, file_path):

    with pytest.raises(NotImplementedError):
        fx_open_spec(file_path)
