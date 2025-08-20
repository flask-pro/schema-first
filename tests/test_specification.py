from marshmallow import fields
from marshmallow import Schema
import pytest

from src.schema_first.openapi import OpenAPI
from src.schema_first.specification import Specification
from tests.utils import get_schema_from_request


@pytest.mark.parametrize('fx', ['fx_spec_required', 'fx_spec_full'])
def test_specification(request, fx, fx_spec_as_file):
    spec_file = fx_spec_as_file(request.getfixturevalue(fx))
    spec = Specification(spec_file)

    assert isinstance(spec.openapi, OpenAPI)
    assert spec.reassembly_spec is None

    spec.load()

    request_schema = get_schema_from_request(spec.reassembly_spec, '/endpoint', '200')
    assert isinstance(request_schema(), Schema)
    assert isinstance(request_schema().fields['message'], fields.String)
    assert request_schema().load({'message': 'Valid string'})
