from schema_first.openapi.schemas.v3_1_1.parameter_object_schema import ParameterObjectSchema


def test_parameter_required(fx_parameter_object_required):
    ParameterObjectSchema().load(fx_parameter_object_required)


def test_parameter_full(fx_parameter_object_full):
    ParameterObjectSchema().load(fx_parameter_object_full)
