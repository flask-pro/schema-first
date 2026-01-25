from marshmallow import fields
from marshmallow import validate
from marshmallow import validates_schema
from marshmallow import ValidationError

from ..base import BaseSchema
from ..base import DocStringFields
from .schema_object_schema import SchemaObjectSchema


class ExampleSchema(DocStringFields, BaseSchema):
    dataValue = fields.Nested(SchemaObjectSchema)
    serializedValue = fields.String(validate=validate.Length(min=1))
    externalValue = fields.String(validate=validate.Length(min=1))

    @validates_schema
    def validate_exclusive(self, data, **kwargs) -> None:
        if 'serializedValue' in data and 'externalValue' in data:
            raise ValidationError(
                'The <serializedValue> field is mutually exclusive of the <externalValue> field.'
            )
