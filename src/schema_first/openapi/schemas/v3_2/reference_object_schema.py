from ..base import BaseSchema
from ..base import DocStringFields
from ..fields import REF_FIELD


class ReferenceObjectSchema(DocStringFields, BaseSchema):
    ref = REF_FIELD
