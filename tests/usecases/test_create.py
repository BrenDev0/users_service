import pytest

from src.models import UserCreate
from src.usecases import handle_create_user
from src.schemas import UserCreateRequest, UserResponse

@pytest.fixture
def mock_create_request():
    return UserCreateRequest(
        email="email@email.com",
        password="password"
    )

async def test_success(
    mock_encryption_service, 
    mock_hashing_service,
    mock_user,
    mock_create_user,
    mock_create_request
):
    mock_create_user.return_value = mock_user
    mock_encryption_service.encrypt.return_value = "encrypted"
    mock_hashing_service.hash_password.return_value = "hashed"
    mock_hashing_service.deterministic_hash.return_value = "dhashed"
    mock_encryption_service.decrypt.return_value = "decrypted"

    result = await handle_create_user(
        user_data=mock_create_request,
        encryption=mock_encryption_service,
        hashing=mock_hashing_service,
        create_user=mock_create_user
    )

    assert isinstance(result, UserResponse)
    assert result.email == "decrypted"
    mock_encryption_service.encrypt.assert_called_once_with("email@email.com")
    mock_hashing_service.deterministic_hash.assert_called_once_with("email@email.com")
    mock_hashing_service.hash_password.assert_called_once_with("password")
    mock_encryption_service.decrypt.assert_called_once_with("encrypted")

    create_user_call_arg = mock_create_user.await_args.args[0]
    assert isinstance(create_user_call_arg, UserCreate)

    assert create_user_call_arg.email_hash == "dhashed"
    assert create_user_call_arg.password == "hashed"
    assert create_user_call_arg.email == "encrypted"