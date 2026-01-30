from schema_first.openapi.schemas.v3_1_1.operation_object_schema import OperationObjectSchema


def test_operation_schema_required(fx_operation_object_required):
    OperationObjectSchema().load(fx_operation_object_required)


def test_operation_schema_full(fx_operation_object_full):
    OperationObjectSchema().load(fx_operation_object_full)
