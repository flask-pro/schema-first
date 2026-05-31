from schema_first.openapi.schemas.v3_2.parameter_object_schema import ParameterObjectSchema


def test_parameter_required(fx_parameter_object_from_path_required):
    ParameterObjectSchema().load(fx_parameter_object_from_path_required)


def test_parameter_full(fx_parameter_object_from_path_full):
    ParameterObjectSchema().load(fx_parameter_object_from_path_full)
