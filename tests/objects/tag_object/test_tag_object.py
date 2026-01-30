from marshmallow.exceptions import ValidationError
import pytest

from schema_first.openapi.schemas.v3_1_1.tag_object_schema import TagObjectSchema


def test_tag_schema_required(fx_tag_object_required):
    TagObjectSchema().load(fx_tag_object_required)


def test_tag_schema_full(fx_tag_object_full):
    TagObjectSchema().load(fx_tag_object_full)


def test_tag_schema_bad_kind(fx_tag_object_full):
    fx_tag_object_full['kind'] = 'bad_kind'

    with pytest.raises(ValidationError):
        TagObjectSchema().load(fx_tag_object_full)
