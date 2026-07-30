import logging
from uuid import UUID
from fastapi import Request, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from .repository import create, get_by_id, get_by_email_hash, delete_by_id
from ..types import CreateUserFn, GetUserByIdFn, GetUserByEmailHashFn, DeleteUserByIdFn
from ..models import UserCreate, User
from .core import session_maker
logger = logging.getLogger(__name__)

def get_db_session(request: Request):
    session = getattr(request.state, "db", None)

    if not session:
        logging.warning("Request state does not have a valid db session")
        session = session_maker()
    
    return session


def provide_create_user(db: AsyncSession = Depends(get_db_session)) -> CreateUserFn:
    async def create_user(domain_create: UserCreate) -> User:
        return await create(db=db, domain_create=domain_create)
    
    return create_user

def provide_get_user_by_id(db: AsyncSession = Depends(get_db_session)) -> GetUserByIdFn:
    async def get_user_by_id(user_id: UUID) -> User | None:
        return await get_by_id(db=db, user_id=user_id)
    
    return get_user_by_id

def provide_get_user_by_email_hash(db: AsyncSession = Depends(get_db_session)) -> GetUserByEmailHashFn:
    async def get_user_by_email_hash(email_hash: str) -> User | None:
        return await get_by_email_hash(db=db, email_hash=email_hash)

    return get_user_by_email_hash

def provide_delete_user_by_id(db: AsyncSession = Depends(get_db_session)) -> DeleteUserByIdFn:
    async def delete_user_by_id(user_id: UUID) -> bool:
        return await delete_by_id(db=db, user_id=user_id)
    
    return delete_user_by_id
    
