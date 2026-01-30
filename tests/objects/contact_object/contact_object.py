from schema_first.openapi.schemas.v3_1_1.contact_object_schema import ContactObjectSchema


def test_contact_schema__required(fx_contact_object__required):
    ContactObjectSchema().load(fx_contact_object__required)


def test_contact_schema__full(fx_contact_object__full):
    ContactObjectSchema().load(fx_contact_object__full)
