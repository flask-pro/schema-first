import pytest


@pytest.fixture
def fx_field_string__required() -> dict:
    return {'type': 'string'}


@pytest.fixture
def fx_field_string__full(fx_field_string__required) -> dict:
    return {
        **fx_field_string__required,
        'nullable': True,
        'minLength': 0,
        'maxLength': 20,
        'pattern': r'^[\d\w\s\S]*$',
        'description': 'Example to message field.',
        'default': 'String field.',
    }


@pytest.fixture
def fx_field_string__binary(fx_field_string__required) -> dict:
    return {
        **fx_field_string__required,
        'format': 'binary',
        'minLength': 0,
        'maxLength': 20,
        'default': '0b1',
    }


@pytest.fixture
def fx_field_string__date(fx_field_string__required) -> dict:
    return {
        **fx_field_string__required,
        'format': 'date',
        'minLength': 0,
        'maxLength': 20,
        'default': '2025-01-01',
    }


@pytest.fixture
def fx_field_string__date_time(fx_field_string__required) -> dict:
    return {
        **fx_field_string__required,
        'format': 'date-time',
        'minLength': 0,
        'maxLength': 20,
        'default': '2025-01-01T00:00:00Z',
    }


@pytest.fixture
def fx_field_string__email(fx_field_string__required) -> dict:
    return {
        **fx_field_string__required,
        'format': 'email',
        'minLength': 0,
        'maxLength': 20,
        'default': 'email@email.email',
    }


@pytest.fixture
def fx_field_string__ipv4(fx_field_string__required) -> dict:
    return {
        **fx_field_string__required,
        'format': 'ipv4',
        'minLength': 0,
        'maxLength': 20,
        'default': '192.168.0.0',
    }


@pytest.fixture
def fx_field_string__ipv6(fx_field_string__required) -> dict:
    return {
        **fx_field_string__required,
        'format': 'ipv6',
        'minLength': 0,
        'maxLength': 20,
        'default': 'fa:de:ef:fe:c7::0',
    }


@pytest.fixture
def fx_field_string__time(fx_field_string__required) -> dict:
    return {
        **fx_field_string__required,
        'format': 'time',
        'minLength': 0,
        'maxLength': 20,
        'default': '00:00:00',
    }


@pytest.fixture
def fx_field_string__uri(fx_field_string__required) -> dict:
    return {
        **fx_field_string__required,
        'format': 'uri',
        'minLength': 0,
        'maxLength': 20,
        'default': 'http://legalact.pro',
    }


@pytest.fixture
def fx_field_string__uuid(fx_field_string__required) -> dict:
    return {
        **fx_field_string__required,
        'format': 'uuid',
        'minLength': 36,
        'maxLength': 36,
        'default': '261da395-0b75-44d7-8b28-c63d4192316b',
    }
