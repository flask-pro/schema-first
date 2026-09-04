from marshmallow.exceptions import ValidationError
import pytest


def test_integer_field(fx_openapi_3_2_0, fx_open_spec):
    file_path = fx_openapi_3_2_0('schemas/integer.yaml')
    spec = fx_open_spec(file_path)

    schema = spec.reassembly_spec['paths']['/endpoint']['get']['responses']['200']['content'][
        'application/json'
    ]['schema']

    with pytest.raises(ValidationError) as exc:
        schema().load({'field': -2})
    assert exc.value.args[0] == {
        'field': ['Must be greater than or equal to -1 and less than or equal to 1.']
    }

    schema().load({'field': 0})

    with pytest.raises(ValidationError) as exc:
        schema().load({'field': 2})
    assert exc.value.args[0] == {
        'field': ['Must be greater than or equal to -1 and less than or equal to 1.']
    }
