from pathlib import Path

from marshmallow import fields
from marshmallow import Schema
from openapi_spec_validator import validate as osv_validate
from openapi_spec_validator.readers import read_from_filename
import pytest

from src.schema_first.openapi import OpenAPI
from src.schema_first.specification import Specification
from tests.conftest import tests_dir_abspath
from tests.utils import get_schema_from_request

specs_base_dir = Path(tests_dir_abspath, '_contrib', 'specs')
spec_file_paths = list(Path(specs_base_dir, 'v3.0').iterdir())
spec_file_paths.extend(list(Path(specs_base_dir, 'v3.1').iterdir()))
spec_file_paths.extend(list(Path(specs_base_dir, 'v3.2').iterdir()))


@pytest.mark.parametrize('fx', ['fx_spec_required', 'fx_spec_full'])
def test_specification(request, fx_spec_as_file, fx):
    spec_file = fx_spec_as_file(request.getfixturevalue(fx))
    spec = Specification(spec_file)

    assert isinstance(spec.openapi, OpenAPI)
    assert spec.reassembly_spec is None

    spec.load()

    request_schema = get_schema_from_request(spec.reassembly_spec, '/endpoint', '200')
    assert isinstance(request_schema(), Schema)
    assert isinstance(request_schema().fields['message'], fields.String)
    assert request_schema().load({'message': 'Valid string'})


@pytest.mark.xfail(reason='Schema specification not fully realisation.')
@pytest.mark.parametrize('file_path', spec_file_paths, ids=map(str, spec_file_paths))
def test_specification_from_file(file_path):
    spec_as_dict, _ = read_from_filename(file_path)
    osv_validate(spec_as_dict)

    spec = Specification(file_path)
    spec.load()
