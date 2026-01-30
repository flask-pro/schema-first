import pytest


@pytest.fixture
def fx_path_item_object_required(fx_operation_object_required) -> dict:
    return {'get': fx_operation_object_required}


@pytest.fixture
def fx_path_item_object_full(
    fx_path_item_object_required, fx_operation_object_full, fx_server_object_full
) -> dict:
    return {
        **fx_path_item_object_required,
        'description': 'Returns pets based on ID',
        'summary': 'Find pets by ID',
        'get': fx_operation_object_full,
        'put': fx_operation_object_full,
        'post': fx_operation_object_full,
        'delete': fx_operation_object_full,
        'options': fx_operation_object_full,
        'head': fx_operation_object_full,
        'patch': fx_operation_object_full,
        'trace': fx_operation_object_full,
        'query': fx_operation_object_full,
        'servers': [fx_server_object_full],
    }
