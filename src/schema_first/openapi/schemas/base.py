from marshmallow import RAISE
from marshmallow import Schema

from schema_first.openapi.schemas.fields import DESCRIPTION_FIELD
from schema_first.openapi.schemas.fields import SUMMARY_FIELD


class BaseSchema(Schema):
    class Meta:
        unknown = RAISE


class DocStringFields(Schema):
    summary = SUMMARY_FIELD
    description = DESCRIPTION_FIELD
