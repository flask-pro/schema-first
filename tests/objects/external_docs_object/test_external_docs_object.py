from marshmallow.exceptions import ValidationError
import pytest

from schema_first.openapi.schemas.v3_1_1.external_docs_schema import ExternalDocsSchema


def test_external_docs_schema_required(fx_external_docs_object_required):
    ExternalDocsSchema().load(fx_external_docs_object_required)


def test_external_docs_schema_full(fx_external_docs_object_full):
    ExternalDocsSchema().load(fx_external_docs_object_full)


def test_external_docs_schema__validate_mutual(fx_external_docs_object_full):
    fx_external_docs_object_full['identifier'] = 'Apache-2.0'
    with pytest.raises(ValidationError):
        ExternalDocsSchema().load(fx_external_docs_object_full)
