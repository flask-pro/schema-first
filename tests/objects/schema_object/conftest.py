import pytest


@pytest.fixture
def fx_schema_object__required(fx_field_string__required) -> dict:
    return {
        'type': 'object',
        'properties': {'message': fx_field_string__required},
    }


@pytest.fixture
def fx_schema_object__full(
    fx_schema_object__required,
    fx_field_string__full,
    fx_field_string__binary,
    fx_field_string__date,
    fx_field_string__date_time,
    fx_field_string__email,
    fx_field_string__ipv4,
    fx_field_string__ipv6,
    fx_field_string__time,
    fx_field_string__uri,
    fx_field_string__uuid,
) -> dict:
    return {
        **fx_schema_object__required,
        'required': ['message'],
        'nullable': False,
        'additionalProperties': False,
        'properties': {
            'message': fx_field_string__full,
            'binary': fx_field_string__binary,
            'date': fx_field_string__date,
            'date-time': fx_field_string__date_time,
            'email': fx_field_string__email,
            'ipv4': fx_field_string__ipv4,
            'ipv6': fx_field_string__ipv6,
            'time': fx_field_string__time,
            'uri': fx_field_string__uri,
            'uuid': fx_field_string__uuid,
        },
    }
