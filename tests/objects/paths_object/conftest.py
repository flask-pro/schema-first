import pytest


@pytest.fixture
def fx_paths_object__required(fx_path_item_object__required) -> dict:
    return {'/required-endpoint': fx_path_item_object__required}


@pytest.fixture
def fx_paths_object__full(fx_paths_object__required, fx_path_item_object__full) -> dict:
    return {**fx_paths_object__required, '/full-endpoint': fx_path_item_object__full}
