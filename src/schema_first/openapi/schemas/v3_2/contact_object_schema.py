from marshmallow import fields

from schema_first.openapi.schemas.base import BaseSchema


class ContactObjectSchema(BaseSchema):
    name = fields.String()
    url = fields.URL()
    email = fields.Email()
