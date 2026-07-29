from marshmallow import fields
from marshmallow.exceptions import ValidationError
import pytest

from src.schema_first.specification import Specification
from tests.utils import get_schema_from_request


def test_converter__schema_fields(fx_spec_full, fx_spec_as_file):
    spec_file = fx_spec_as_file(fx_spec_full)
    spec = Specification(spec_file).load()
    request_schema = get_schema_from_request(spec.reassembly_spec, '/full-endpoint', '200')

    assert isinstance(request_schema().fields['message'], fields.String)
    assert isinstance(request_schema().fields['binary'], fields.String)
    assert isinstance(request_schema().fields['date'], fields.Date)
    assert isinstance(request_schema().fields['date-time'], fields.AwareDateTime)
    assert isinstance(request_schema().fields['email'], fields.Email)
    assert isinstance(request_schema().fields['ipv4'], fields.IPv4)
    assert isinstance(request_schema().fields['ipv6'], fields.IPv6)
    assert isinstance(request_schema().fields['time'], fields.Time)
    assert isinstance(request_schema().fields['uri'], fields.URL)
    assert isinstance(request_schema().fields['uuid'], fields.UUID)

    assert request_schema().load({'message': 'Valid string'})


@pytest.mark.parametrize(
    'schema',
    [
        {'message': 'Valid string'},
        {'binary': 'Valid binary'},
        {'email': 'test@test.test'},
        {'uri': 'https://test.test/test'},
    ],
)
def test_converter__string_valid(fx_spec_full, fx_spec_as_file, schema):
    spec_file = fx_spec_as_file(fx_spec_full)
    spec = Specification(spec_file).load()
    request_schema = get_schema_from_request(spec.reassembly_spec, '/full-endpoint', '200')

    schema['message'] = 'Valid string'
    request_schema().load(schema)


@pytest.mark.parametrize(
    'schema',
    [
        {'message': 1},
        {'binary': 1},
        {'date': 'Invalid date'},
        {'date-time': 'Invalid date-time'},
        {'email': 'Invalid email'},
        {'ipv4': 'Invalid ipv4'},
        {'ipv6': 'Invalid ipv6'},
        {'time': 'Invalid time'},
        {'uri': 'Invalid uri'},
        {'uuid': 'Invalid uuid'},
    ],
)
def test_converter__string_not_valid(fx_spec_full, fx_spec_as_file, schema):
    spec_file = fx_spec_as_file(fx_spec_full)
    spec = Specification(spec_file).load()
    request_schema = get_schema_from_request(spec.reassembly_spec, '/full-endpoint', '200')

    with pytest.raises(ValidationError):
        request_schema().load(schema)


@pytest.mark.parametrize('schema', [{'message': None}])
def test_converter__string_nullable(fx_spec_full, fx_spec_as_file, schema):
    spec_file = fx_spec_as_file(fx_spec_full)
    spec = Specification(spec_file).load()
    request_schema = get_schema_from_request(spec.reassembly_spec, '/full-endpoint', '200')

    request_schema().load(schema)
