from marshmallow.exceptions import ValidationError
import pytest

from schema_first.openapi.schemas.v3_1_1.schema_object_schema import SchemaObjectSchema


@pytest.mark.parametrize('fixture', ['fx_field_number__required', 'fx_field_number__full'])
def test_number_field(request, fixture):
    SchemaObjectSchema().load(request.getfixturevalue(fixture))


@pytest.mark.parametrize(
    'value,message',
    [
        ('Bad number.', "{'default': ['Not a valid number.']}"),
        (None, "{'default': ['Field may not be null.']}"),
    ],
)
def test_number_field__default__type(fx_field_number__full, value, message):
    fx_field_number__full['default'] = value

    with pytest.raises(ValidationError) as e:
        SchemaObjectSchema().load(fx_field_number__full)

    assert str(e.value) == message


@pytest.mark.parametrize('value', [-11.1, -6.6, 6.6, 11.1])
def test_number_field__default__value(fx_field_number__full, value):
    fx_field_number__full['minimum'] = -10
    fx_field_number__full['exclusiveMinimum'] = -5
    fx_field_number__full['exclusiveMaximum'] = 5
    fx_field_number__full['maximum'] = 10
    fx_field_number__full['default'] = value

    with pytest.raises(ValidationError):
        SchemaObjectSchema().load(fx_field_number__full)
