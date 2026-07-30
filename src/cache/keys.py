from uuid import UUID


def get_current_user_key(user_id: UUID) -> str:
    return f"{user_id}:auth:current_user"
