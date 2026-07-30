import pytest

from uuid import uuid4
from src.users.usecases import handle_delete_user_by_id
from src.cache.keys import get_current_user_key


async def test_success(mock_delete_user_by_id, mock_cache_store):
    mock_delete_user_by_id.return_value = True
    user_id = uuid4()

    result = await handle_delete_user_by_id(
        user_id=user_id,
        delete_user_by_id=mock_delete_user_by_id,
        cache_store=mock_cache_store
    )

    assert result is True
    mock_delete_user_by_id.assert_called_once_with(user_id)
    mock_cache_store.remove.assert_called_once_with(get_current_user_key(user_id))


async def test_not_found(mock_delete_user_by_id, mock_cache_store):
    mock_delete_user_by_id.return_value = False
    user_id = uuid4()

    result = await handle_delete_user_by_id(
        user_id=user_id,
        delete_user_by_id=mock_delete_user_by_id,
        cache_store=mock_cache_store
    )

    assert result is False
    mock_delete_user_by_id.assert_called_once_with(user_id)
    mock_cache_store.remove.assert_not_called()
