import pytest


@pytest.fixture
def fx_info_object_required() -> dict:
    return {'title': 'Example Pet Store App (API for testing Flask-First)', 'version': '1.0.1'}


@pytest.fixture
def fx_info_object_full(
    fx_info_object_required, fx_contact_object_full, fx_license_object_full
) -> dict:
    return {
        **fx_info_object_required,
        'summary': 'A pet store manager.',
        'description': 'This is an example server for a pet store.',
        'termsOfService': 'https://example.com/terms/',
        'contact': fx_contact_object_full,
        'license': fx_license_object_full,
    }
