from uuid import UUID
from fastapi import APIRouter, Depends, HTTPException
from .schemas import UserResponse
from .usecases import handle_get_user_by_id, handle_delete_user_by_id
from .types import GetUserByIdFn, DeleteUserByIdFn
from ..cryptography.types import EncryptionService
from ..cryptography.dependencies import get_encryption_service
from ..cache.types import CacheStore
from ..cache.dependencies import get_cache_store
from .sqlalchemy.dependencies import provide_get_user_by_id, provide_delete_user_by_id

router = APIRouter(
    tags=["Users"]
)

@router.get("/{user_id}", status_code=200, response_model=UserResponse)
async def users_get(
    user_id: UUID,
    encryption_service: EncryptionService = Depends(get_encryption_service),
    get_user_by_id: GetUserByIdFn = Depends(provide_get_user_by_id)
):
    user = await handle_get_user_by_id(
        user_id=user_id,
        encryption=encryption_service,
        get_user_by_id=get_user_by_id
    )

    if not user:
        raise HTTPException(status_code=404, detail="User not found")

    return user

@router.delete("/{user_id}", status_code=204)
async def users_delete(
    user_id: UUID,
    delete_user_by_id: DeleteUserByIdFn = Depends(provide_delete_user_by_id),
    cache_store: CacheStore = Depends(get_cache_store)
):
    deleted = await handle_delete_user_by_id(
        user_id=user_id,
        delete_user_by_id=delete_user_by_id,
        cache_store=cache_store
    )

    if not deleted:
        raise HTTPException(status_code=404, detail="User not found")