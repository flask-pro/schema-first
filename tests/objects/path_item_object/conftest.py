import pytest


@pytest.fixture
def fx_path_item_object__required(fx_operation_object__required) -> dict:
    return {'get': fx_operation_object__required}


@pytest.fixture
def fx_path_item_object__full(
    fx_path_item_object__required, fx_operation_object__full, fx_server_object_full
) -> dict:
    return {
        **fx_path_item_object__required,
        'description': 'Returns pets based on ID',
        'summary': 'Find pets by ID',
        'get': fx_operation_object__full,
        'put': fx_operation_object__full,
        'post': fx_operation_object__full,
        'delete': fx_operation_object__full,
        'options': fx_operation_object__full,
        'head': fx_operation_object__full,
        'patch': fx_operation_object__full,
        'trace': fx_operation_object__full,
        'query': fx_operation_object__full,
        'servers': [fx_server_object_full],
    }
