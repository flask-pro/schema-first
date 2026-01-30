from marshmallow.exceptions import ValidationError
import pytest

from schema_first.openapi.schemas.v3_1_1.server_object_schema import ServerObjectSchema


def test_server_schema_required(fx_server_object_required):
    ServerObjectSchema().load(fx_server_object_required)


def test_server_schema_full(fx_server_object_full):
    ServerObjectSchema().load(fx_server_object_full)


@pytest.mark.parametrize(
    'value', ['http://', 'https://', '/', 'https://legalact.pro', 'https://легалакт.рф']
)
def test_server_schema__validation_url__valid(fx_server_object_required, value):
    fx_server_object_required['url'] = value
    ServerObjectSchema().load(fx_server_object_required)


@pytest.mark.parametrize('value', [None, '', ' ', 'NOT_VALID', '/ /'])
def test_server_schema__validation_url__not_valid(fx_server_object_required, value):
    fx_server_object_required['url'] = value

    with pytest.raises(ValidationError):
        ServerObjectSchema().load(fx_server_object_required)
