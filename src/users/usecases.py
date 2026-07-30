from uuid import UUID
from .schemas import UserResponse
from .types import GetUserByIdFn, DeleteUserByIdFn
from ..cryptography.types import EncryptionService
from ..cache.types import CacheStore
from ..cache.keys import get_current_user_key
from ..mappers import domain_to_public_schema



async def handle_get_user_by_id(
    user_id: UUID,
    encryption: EncryptionService,
    get_user_by_id: GetUserByIdFn
) -> UserResponse | None:
    user = await get_user_by_id(user_id)

    if not user:
        return None

    return domain_to_public_schema(domain=user, decrypt=encryption.decrypt)


async def handle_delete_user_by_id(
    user_id: UUID,
    delete_user_by_id: DeleteUserByIdFn,
    cache_store: CacheStore
) -> bool:
    deleted = await delete_user_by_id(user_id)

    if deleted:
        await cache_store.remove(get_current_user_key(user_id))

    return deleted