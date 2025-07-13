import pytest
from marshmallow.exceptions import ValidationError
from schema_first.openapi.schemas.v3_1_1.license_schema import LicenseSchema


def test_server_schema_minimal(fx_license_object_minimal):
    LicenseSchema().load(fx_license_object_minimal)


def test_server_schema_full(fx_license_object_full):
    LicenseSchema().load(fx_license_object_full)


def test_server_schema__validate_mutual(fx_license_object_full):
    fx_license_object_full['identifier'] = 'Apache-2.0'
    with pytest.raises(ValidationError):
        LicenseSchema().load(fx_license_object_full)
