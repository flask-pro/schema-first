from marshmallow import fields

from ..base import BaseSchema


class ContactSchema(BaseSchema):
    name = fields.String()
    url = fields.URL()
    email = fields.Email()
