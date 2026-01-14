from marshmallow.exceptions import ValidationError
import pytest

from schema_first.openapi.schemas.v3_1_1.schema_object_schema import SchemaObjectSchema


@pytest.mark.parametrize('fixture', ['fx_field_integer__required', 'fx_field_integer__full'])
def test_integer_field(request, fixture):
    SchemaObjectSchema().load(request.getfixturevalue(fixture))


@pytest.mark.parametrize(
    'value,message',
    [
        ('Bad integer.', "{'default': ['Not a valid integer.']}"),
        (None, "{'default': ['Field may not be null.']}"),
    ],
)
def test_integer_field__default__type(fx_field_integer__full, value, message):
    fx_field_integer__full['default'] = value

    with pytest.raises(ValidationError) as e:
        SchemaObjectSchema().load(fx_field_integer__full)

    assert str(e.value) == message


@pytest.mark.parametrize('value', [-11, -6, 6, 11])
def test_integer_field__default__value(fx_field_integer__full, value):
    fx_field_integer__full['minimum'] = -10
    fx_field_integer__full['exclusiveMinimum'] = -5
    fx_field_integer__full['exclusiveMaximum'] = 5
    fx_field_integer__full['maximum'] = 10
    fx_field_integer__full['default'] = value

    with pytest.raises(ValidationError):
        SchemaObjectSchema().load(fx_field_integer__full)
