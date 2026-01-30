from schema_first.openapi.schemas.v3_1_1.contact_object_schema import ContactObjectSchema


def test_contact_schema_required(fx_contact_object_required):
    ContactObjectSchema().load(fx_contact_object_required)


def test_contact_schema_full(fx_contact_object_full):
    ContactObjectSchema().load(fx_contact_object_full)
