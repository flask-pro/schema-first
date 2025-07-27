from marshmallow import fields

from src.schema_first.openapi import OpenAPI
from src.schema_first.specification import Specification
from tests.utils import get_schema_from_request


def test_specification__minimal(fx_spec_minimal, fx_spec_as_file):
    spec_file = fx_spec_as_file(fx_spec_minimal)
    spec = Specification(spec_file)

    assert isinstance(spec.openapi, OpenAPI)
    assert spec.reassembly_spec is None

    spec.load()

    request_schema = get_schema_from_request(spec.reassembly_spec, '/endpoint', '200')
    assert isinstance(request_schema().fields['message'], fields.String)
    assert request_schema().load({'message': 'Valid string'})


def test_specification__full(fx_spec_full, fx_spec_as_file):
    spec_file = fx_spec_as_file(fx_spec_full)
    spec = Specification(spec_file)

    assert isinstance(spec.openapi, OpenAPI)
    assert spec.reassembly_spec is None

    spec.load()

    request_schema = get_schema_from_request(spec.reassembly_spec, '/endpoint', '200')
    assert isinstance(request_schema().fields['message'], fields.String)
    assert request_schema().load({'message': 'Valid string'})
