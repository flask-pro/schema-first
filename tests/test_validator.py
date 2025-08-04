import pytest

from src.schema_first.openapi import OpenAPI
from src.schema_first.openapi import OpenAPIValidationError


def test_validator_required(fx_spec_required, fx_spec_as_file):
    spec_file = fx_spec_as_file(fx_spec_required)
    open_api_spec = OpenAPI(spec_file)
    open_api_spec.load()
    assert open_api_spec.raw_spec == fx_spec_required


def test_validator__full(fx_spec_full, fx_spec_as_file):
    spec_file = fx_spec_as_file(fx_spec_full)
    open_api_spec = OpenAPI(spec_file)
    open_api_spec.load()
    assert open_api_spec.raw_spec == fx_spec_full


def test_validator__required__external_validator(fx_spec_required, fx_spec_as_file):
    spec_file = fx_spec_as_file(fx_spec_required, external_validator=True)
    open_api_spec = OpenAPI(spec_file)
    open_api_spec.load()


def test_validator__full__external_validator(fx_spec_full, fx_spec_as_file):
    spec_file = fx_spec_as_file(fx_spec_full, external_validator=True)
    open_api_spec = OpenAPI(spec_file)
    open_api_spec.load()


def test_validator__wrong_field_name(fx_spec_required, fx_spec_as_file):
    fx_spec_required['wrong_field_name'] = 'wrong'

    spec_file = fx_spec_as_file(fx_spec_required)

    open_api_spec = OpenAPI(spec_file)

    with pytest.raises(OpenAPIValidationError):
        open_api_spec.load()
