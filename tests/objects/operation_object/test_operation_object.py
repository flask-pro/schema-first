from schema_first.openapi.schemas.v3_1_1.operation_object_schema import OperationObjectSchema


def test_operation_schema__required(fx_operation_object__required):
    OperationObjectSchema().load(fx_operation_object__required)


def test_operation_schema__full(fx_operation_object__full):
    OperationObjectSchema().load(fx_operation_object__full)
