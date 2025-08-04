from marshmallow.exceptions import ValidationError
import pytest

from schema_first.openapi.schemas.v3_1_1.server_schema import ServerSchema


def test_server_schema_required(fx_server_object_required):
    ServerSchema().load(fx_server_object_required)


def test_server_schema_full(fx_server_object_full):
    ServerSchema().load(fx_server_object_full)


@pytest.mark.parametrize(
    'value', ['http://', 'https://', '/', 'https://legalact.pro', 'https://легалакт.рф']
)
def test_server_schema__validation_url__valid(fx_server_object_required, value):
    fx_server_object_required['url'] = value
    ServerSchema().load(fx_server_object_required)


@pytest.mark.parametrize('value', [None, '', ' ', 'NOT_VALID', '/ /'])
def test_server_schema__validation_url__not_valid(fx_server_object_required, value):
    fx_server_object_required['url'] = value

    with pytest.raises(ValidationError):
        ServerSchema().load(fx_server_object_required)
