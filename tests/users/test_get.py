import pytest

from uuid import uuid4
from src.users.usecases import handle_get_user_by_id
from src.users.schemas import UserResponse


async def test_success(
    mock_encryption_service,
    mock_user,
    mock_get_user_by_id
):
    mock_get_user_by_id.return_value = mock_user
    mock_encryption_service.decrypt.return_value = "decrypted"

    result = await handle_get_user_by_id(
        user_id=mock_user.id,
        encryption=mock_encryption_service,
        get_user_by_id=mock_get_user_by_id
    )

    assert isinstance(result, UserResponse)
    assert result.email == "decrypted"
    mock_get_user_by_id.assert_called_once_with(mock_user.id)
    mock_encryption_service.decrypt.assert_called_once_with(mock_user.email)


async def test_not_found(
    mock_encryption_service,
    mock_get_user_by_id
):
    mock_get_user_by_id.return_value = None
    user_id = uuid4()

    result = await handle_get_user_by_id(
        user_id=user_id,
        encryption=mock_encryption_service,
        get_user_by_id=mock_get_user_by_id
    )

    assert result is None
    mock_get_user_by_id.assert_called_once_with(user_id)
    mock_encryption_service.decrypt.assert_not_called()
