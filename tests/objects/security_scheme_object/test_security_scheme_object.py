import pytest

from schema_first.openapi.schemas.v3_2.security_scheme_object_schema import (
    SecuritySchemeObjectSchema,
)


@pytest.mark.parametrize(
    'fixture',
    ['fx_security_scheme_object_basic_required', 'fx_security_scheme_object_bearer_required'],
)
def test_info_object_schema_required(request, fixture):
    SecuritySchemeObjectSchema().load(request.getfixturevalue(fixture))


@pytest.mark.parametrize(
    'fixture', ['fx_security_scheme_object_basic_full', 'fx_security_scheme_object_bearer_full']
)
def test_info_object_schema_full(request, fixture):
    SecuritySchemeObjectSchema().load(request.getfixturevalue(fixture))
