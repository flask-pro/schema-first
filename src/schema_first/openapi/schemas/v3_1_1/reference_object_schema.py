from schema_first.openapi.schemas._base import BaseSchema
from schema_first.openapi.schemas._fields import DESCRIPTION_FIELD
from schema_first.openapi.schemas._fields import REF_FIELD


class ReferenceObjectSchema(BaseSchema):
    description = DESCRIPTION_FIELD
    ref = REF_FIELD
