from marshmallow import fields
import pytest

from src.schema_first.openapi import OpenAPI
from src.schema_first.openapi import OpenAPIValidationError
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
    open_api_spec = OpenAPI(spec_file)
    open_api_spec.load()
    assert open_api_spec.raw_spec == fx_spec_full


def test_specification__minimal__external_validator(fx_spec_minimal, fx_spec_as_file):
    spec_file = fx_spec_as_file(fx_spec_minimal, external_validator=True)
    open_api_spec = OpenAPI(spec_file)
    open_api_spec.load()


def test_specification__full__external_validator(fx_spec_full, fx_spec_as_file):
    spec_file = fx_spec_as_file(fx_spec_full, external_validator=True)
    open_api_spec = OpenAPI(spec_file)
    open_api_spec.load()


def test_specification__wrong_field_name(fx_spec_minimal, fx_spec_as_file):
    fx_spec_minimal['wrong_field_name'] = 'wrong'

    spec_file = fx_spec_as_file(fx_spec_minimal)

    open_api_spec = OpenAPI(spec_file)

    with pytest.raises(OpenAPIValidationError):
        open_api_spec.load()
