import pytest
from marshmallow.exceptions import ValidationError
from schema_first.openapi.schemas.v3_1_1.server_schema import ServerSchema


def test_server_schema_minimal(fx_server_object_minimal):
    ServerSchema().load(fx_server_object_minimal)


def test_server_schema_full(fx_server_object_full):
    ServerSchema().load(fx_server_object_full)


@pytest.mark.parametrize(
    'value', ['http://', 'https://', '/', 'https://legalact.pro', 'https://легалакт.рф']
)
def test_server_schema__validation_url__valid(fx_server_object_minimal, value):
    fx_server_object_minimal['url'] = value
    ServerSchema().load(fx_server_object_minimal)


@pytest.mark.parametrize('value', [None, '', ' ', 'NOT_VALID', '/ /'])
def test_server_schema__validation_url__not_valid(fx_server_object_minimal, value):
    fx_server_object_minimal['url'] = value

    with pytest.raises(ValidationError):
        ServerSchema().load(fx_server_object_minimal)
