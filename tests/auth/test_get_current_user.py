from src.auth.usecases import handle_get_current_user
from src.auth.schemas import CurrentUserResponse


def test_success(mock_user):
    result = handle_get_current_user(mock_user)

    assert isinstance(result, CurrentUserResponse)
    assert result.user_id == mock_user.id
