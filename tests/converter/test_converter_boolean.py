from marshmallow import fields
from marshmallow.exceptions import ValidationError
import pytest

from src.schema_first.specification import Specification
from tests.utils import get_schema_from_request


def test_converter__boolean_schema_fields(fx_spec_full, fx_spec_as_file):
    spec_file = fx_spec_as_file(fx_spec_full)
    spec = Specification(spec_file).load()
    request_schema = get_schema_from_request(spec.reassembly_spec, '/endpoint', '200')

    assert isinstance(request_schema().fields['boolean'], fields.Boolean)

    assert request_schema().load({'message': 'Valid string'})


@pytest.mark.parametrize('schema', [{'boolean': True}, {'boolean': False}])
def test_converter__boolean_valid(fx_spec_full, fx_spec_as_file, schema):
    spec_file = fx_spec_as_file(fx_spec_full)
    spec = Specification(spec_file).load()
    request_schema = get_schema_from_request(spec.reassembly_spec, '/endpoint', '200')

    schema['message'] = 'Valid string'
    request_schema().load(schema)


@pytest.mark.parametrize(
    'schema', [{'boolean': 'Invalid string'}, {'boolean': 0.1}, {'boolean': ''}]
)
def test_converter__boolean_not_valid(fx_spec_full, fx_spec_as_file, schema):
    spec_file = fx_spec_as_file(fx_spec_full)
    spec = Specification(spec_file).load()
    request_schema = get_schema_from_request(spec.reassembly_spec, '/endpoint', '200')

    schema['message'] = 'Valid string'
    with pytest.raises(ValidationError) as e:
        request_schema().load(schema)

    assert e.value.messages == {'boolean': ['Not a valid boolean.']}


@pytest.mark.parametrize('schema', [{'boolean': None}])
def test_converter__string_nullable(fx_spec_full, fx_spec_as_file, schema):
    spec_file = fx_spec_as_file(fx_spec_full)
    spec = Specification(spec_file).load()
    request_schema = get_schema_from_request(spec.reassembly_spec, '/endpoint', '200')

    schema['message'] = 'Valid string'
    request_schema().load(schema)
