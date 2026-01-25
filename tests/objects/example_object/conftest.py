import pytest


@pytest.fixture
def fx_example_object_required() -> dict:
    return {}


@pytest.fixture
def fx_example_object_full(fx_example_object_required, fx_schema_object__full) -> dict:
    return {
        **fx_example_object_required,
        'summary': 'A work with an average rating of 4.5 stars',
        'description': 'A work with an average rating of 4.5 stars',
        'dataValue': fx_schema_object__full,
        'serializedValue': '| {"author": "A. Writer", "title": "An Older Book", "rating": 4.5}',
    }
