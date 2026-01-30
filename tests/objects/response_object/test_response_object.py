from schema_first.openapi.schemas.v3_1_1.responses_object_schema import ResponseObjectSchema


def test_responses_schema_required(fx_response_object__required):
    ResponseObjectSchema().load(fx_response_object__required)


def test_responses_schema_full(fx_response_object__full):
    ResponseObjectSchema().load(fx_response_object__full)
