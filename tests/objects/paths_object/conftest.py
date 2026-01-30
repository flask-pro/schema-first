import pytest


@pytest.fixture
def fx_paths_object_required(fx_path_item_object_required) -> dict:
    return {'/required-endpoint': fx_path_item_object_required}


@pytest.fixture
def fx_paths_object_full(fx_paths_object_required, fx_path_item_object_full) -> dict:
    return {**fx_paths_object_required, '/full-endpoint': fx_path_item_object_full}
