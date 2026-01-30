from marshmallow.exceptions import ValidationError
import pytest

from schema_first.openapi.schemas.v3_1_1.license_object_schema import LicenseObjectSchema


def test_license_schema_required(fx_license_object_required):
    LicenseObjectSchema().load(fx_license_object_required)


def test_license_schema_full(fx_license_object_full):
    LicenseObjectSchema().load(fx_license_object_full)


def test_license_schema__validate_mutual(fx_license_object_full):
    fx_license_object_full['identifier'] = 'Apache-2.0'
    with pytest.raises(ValidationError):
        LicenseObjectSchema().load(fx_license_object_full)
