import pytest


@pytest.fixture
def fx_security_requirement_object_full() -> dict[str, list[str]]:
    return {'BasicAuth': ['Anonymous']}
