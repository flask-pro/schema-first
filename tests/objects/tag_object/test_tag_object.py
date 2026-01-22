from marshmallow.exceptions import ValidationError
import pytest

from schema_first.openapi.schemas.v3_1_1.tag_schema import TagSchema


def test_tag_schema_required(fx_tag_object_required):
    TagSchema().load(fx_tag_object_required)


def test_tag_schema_full(fx_tag_object_full):
    TagSchema().load(fx_tag_object_full)


def test_tag_schema_bad_kind(fx_tag_object_full):
    fx_tag_object_full['kind'] = 'bad_kind'

    with pytest.raises(ValidationError):
        TagSchema().load(fx_tag_object_full)
