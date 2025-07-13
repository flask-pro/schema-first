import pytest

from src.schema_first.openapi import OpenAPI
from src.schema_first.openapi import OpenAPIValidationError


def test_specification(fx_spec_minimal, fx_spec_as_file):
    spec_file = fx_spec_as_file(fx_spec_minimal)
    open_api_spec = OpenAPI(spec_file)
    open_api_spec.load()


def test_specification__full(fx_spec_full, fx_spec_as_file):
    spec_file = fx_spec_as_file(fx_spec_full)
    open_api_spec = OpenAPI(spec_file)
    open_api_spec.load()


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
