import pytest


@pytest.fixture
def fx_license_object_minimal() -> dict:
    return {'name': 'Apache 2.0'}


@pytest.fixture
def fx_license_object_full(fx_license_object_minimal) -> dict:
    return {
        **fx_license_object_minimal,
        'url': 'https://www.apache.org/licenses/LICENSE-2.0.txt',
    }
