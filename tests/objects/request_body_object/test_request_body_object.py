from schema_first.openapi.schemas.v3_2.request_body_object_schema import RequestBodyObject


def test_responses_schema_required(fx_request_body_object_required):
    RequestBodyObject().load(fx_request_body_object_required)


def test_responses_schema_full(fx_request_body_object_full):
    RequestBodyObject().load(fx_request_body_object_full)
