from fastapi import APIRouter, Depends
from .schemas import UserResponse, UserCreateRequest
from .usecases import handle_create_user
from .types import CreateUserFn
from .cryptography.types import EncryptionService, HashingService
from .cryptography.dependencies import get_encryption_service, get_hashing_service
from .sqlalchemy.dependencies import provide_create_user

router = APIRouter(
    tags=["Users"]
)

@router.post("", status_code=201, response_model=UserResponse)
async def users_create(
    data: UserCreateRequest,
    encryption_service: EncryptionService = Depends(get_encryption_service),
    hashing_service: HashingService = Depends(get_hashing_service), 
    create_user: CreateUserFn = Depends(provide_create_user)
):
    return await handle_create_user(
        user_data=data,
        encryption=encryption_service,
        hashing=hashing_service,
        create_user=create_user
    )

@router.delete("/{user_id}", status_code=200)
async def users_delete():
    pass