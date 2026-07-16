from .schemas import UserCreateRequest, UserResponse
from .models import UserCreate
from .types import CreateUserFn
from .cryptography.types import HashingService, EncryptionService
from .mappers import domain_to_public_schema

async def handle_create_user(
    user_data: UserCreateRequest,
    encryption: EncryptionService,
    hashing: HashingService,
    create_user: CreateUserFn
) -> UserResponse:
    encrypted_email = encryption.encrypt(user_data.email)
    dhashed_email = hashing.deterministic_hash(user_data.email)

    hashed_password = hashing.hash_password(user_data.password)

    domain_create = UserCreate(
        email=encrypted_email,
        email_hash=dhashed_email,
        password=hashed_password
    )

    new_user = await create_user(domain_create)

    return domain_to_public_schema(domain=new_user, encryption=encryption)