from marshmallow.exceptions import ValidationError
import pytest

from schema_first.openapi.schemas.v3_1_1.external_docs_object_schema import ExternalDocsObjectSchema


def test_external_docs_schema_required(fx_external_docs_object_required):
    ExternalDocsObjectSchema().load(fx_external_docs_object_required)


def test_external_docs_schema_full(fx_external_docs_object_full):
    ExternalDocsObjectSchema().load(fx_external_docs_object_full)


def test_external_docs_schema__validate_mutual(fx_external_docs_object_full):
    fx_external_docs_object_full['identifier'] = 'Apache-2.0'
    with pytest.raises(ValidationError):
        ExternalDocsObjectSchema().load(fx_external_docs_object_full)
