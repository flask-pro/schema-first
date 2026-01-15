from marshmallow import RAISE
from marshmallow import Schema
from marshmallow import validates_schema
from marshmallow import ValidationError

from .fields import DESCRIPTION_FIELD
from .fields import SUMMARY_FIELD


class BaseSchema(Schema):
    class Meta:
        unknown = RAISE

    @validates_schema
    def validate_ref(self, data, **kwargs) -> None:
        if 'ref' in data:
            ALLOWED_FIELDS = {'ref', 'description', 'summary'}
            ALL_FIELDS = set(data.keys())
            if ALL_FIELDS.difference(ALLOWED_FIELDS):
                raise ValidationError(
                    f"If there is a <'ref'> field, then only <{ALLOWED_FIELDS}>,"
                    f" but set <{ALL_FIELDS}>"
                )


class DocStringFields(Schema):
    summary = SUMMARY_FIELD
    description = DESCRIPTION_FIELD
