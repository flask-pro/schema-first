from marshmallow.exceptions import ValidationError
import pytest

from schema_first.openapi.schemas.v3_1_1.schema_object_schema import SchemaObjectSchema


def test_string_field__required(fx_field_string__required):
    SchemaObjectSchema().load(fx_field_string__required)


def test_string_field__full(fx_field_string__full):
    SchemaObjectSchema().load(fx_field_string__full)


def test_string_field__pattern(fx_field_string__required):
    fx_field_string__required['pattern'] = '^*$'

    with pytest.raises(ValidationError) as e:
        SchemaObjectSchema().load(fx_field_string__required)

    assert (
        str(e.value) == "{'pattern': [\"Pattern <^*$> is error"
        " <PatternError('nothing to repeat at position 1')>.\"]}"
    )


def test_string_field__pattern__default(fx_field_string__required):
    fx_field_string__required['pattern'] = r'^\d*$'
    fx_field_string__required['default'] = 'Bad default.'

    with pytest.raises(ValidationError) as e:
        SchemaObjectSchema().load(fx_field_string__required)

    assert str(e.value) == "{'_schema': ['<Bad default.> does not match <^\\\\d*$>']}"


def test_string_field__format__default(fx_field_string__email):
    fx_field_string__email['default'] = 'Bad email.'

    with pytest.raises(ValidationError) as e:
        SchemaObjectSchema().load(fx_field_string__email)

    assert str(e.value) == "{'_schema': [\"{'default': ['Not a valid email address.']}\"]}"
