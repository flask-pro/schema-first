from copy import deepcopy
from pathlib import Path

from marshmallow import fields
from marshmallow import Schema
from openapi_spec_validator import validate as osv_validate
from openapi_spec_validator.readers import read_from_filename
import pytest

from src.schema_first.specification import Specification
from tests.conftest import specs_base_dir
from tests.conftest import tests_dir_abspath
from tests.utils import get_schema_from_request

spec_file_paths = list(Path(specs_base_dir, 'v3.2').iterdir())


@pytest.mark.parametrize('fx', ['fx_spec_required', 'fx_spec_full'])
def test_specification(request, fx_spec_as_file, fx):
    spec_file = fx_spec_as_file(request.getfixturevalue(fx))
    spec = Specification(spec_file)

    assert spec.openapi
    assert spec.reassembly_spec is None

    spec.load()

    request_schema = get_schema_from_request(spec.reassembly_spec, '/required-endpoint', '200')
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


def test_specification__multifile_required(fx_spec_as_file, fx_spec_required):
    endpoint_spec = {'required-endpoint': deepcopy(fx_spec_required['paths']['/required-endpoint'])}
    endpoint_file = fx_spec_as_file(endpoint_spec, file_name='required-endpoint.yaml')

    root_file = fx_spec_required
    root_file['paths']['/required-endpoint'] = {'$ref': f'{endpoint_file.name}#/required-endpoint'}
    spec_file = fx_spec_as_file(root_file)

    spec_as_dict, base_uri = read_from_filename(spec_file)
    osv_validate(spec_as_dict, base_uri=base_uri)

    spec = Specification(spec_file)
    spec.load()


@pytest.mark.xfail(reason='Schema specification not fully realisation.')
def test_specification__multifile():
    file_path = Path(tests_dir_abspath, '_contrib', 'specs', 'v3.2', 'multifile', 'openapi.yaml')
    spec_as_dict, base_uri = read_from_filename(file_path)
    osv_validate(spec_as_dict, base_uri=base_uri)

    spec = Specification(file_path)
    spec.load()
