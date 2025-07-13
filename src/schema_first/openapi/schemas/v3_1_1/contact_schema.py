from marshmallow import fields
from schema_first.openapi.schemas._base import BaseSchema


class ContactSchema(BaseSchema):
    name = fields.String()
    url = fields.URL()
    email = fields.Email()
