from .models import User
from .schemas import UserResponse
from .cryptography.types import EncryptionService


def domain_to_public_schema(domain: User, encryption: EncryptionService) -> UserResponse:
    return UserResponse(
        id=domain.id,
        email=encryption.decrypt(domain.email),
        created_at=domain.created_at
    )
