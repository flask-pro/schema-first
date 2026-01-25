from marshmallow.exceptions import ValidationError
import pytest

from src.schema_first.openapi.schemas.v3_1_1.example_schema import ExampleSchema


def test_example_schema_required(fx_example_object_required):
    ExampleSchema().load(fx_example_object_required)


def test_example_schema_full(fx_example_object_full):
    ExampleSchema().load(fx_example_object_full)


def test_example_schema_bad_kind(fx_example_object_full):
    fx_example_object_full['kind'] = 'bad_kind'

    with pytest.raises(ValidationError):
        ExampleSchema().load(fx_example_object_full)
