import pytest


@pytest.fixture
def fx_server_object_minimal() -> dict:
    return {'url': 'https://{username}.gigantic-server.com:{port}/{basePath}'}


@pytest.fixture
def fx_server_object_full(fx_server_object_minimal) -> dict:
    return {
        **fx_server_object_minimal,
        'description': 'The production API server',
        'variables': {
            'username': {
                'default': 'demo',
                'description': 'A user-specific subdomain. Use `demo` for a free sandbox'
                ' environment.',
            },
            'port': {'enum': ['8443', '443'], 'default': '8443'},
            'basePath': {'default': 'v2'},
        },
    }
