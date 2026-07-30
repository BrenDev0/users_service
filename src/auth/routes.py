from fastapi import APIRouter, Depends, Request, Response
from uuid import UUID
from src.cryptography.dependencies import get_encryption_service, get_hashing_service
from src.cryptography.types import EncryptionService, HashingService
from src.users.sqlalchemy.dependencies import provide_create_user, provide_get_user_by_email_hash
from src.cache.dependencies import get_cache_store
from src.cache.types import CacheStore
from src.users.schemas import UserResponse
from src.users.types import CreateUserFn, GetUserByEmailHashFn
from src.users.models import User
from .schemas import RegistrationRequest, LoginRequest, VerifyEmailRequest, CurrentUserResponse
from .usecases import handle_registration, create_session, handle_login, handle_registration_email_verification, handle_get_current_user
from .dependencies import get_session_id, get_current_user
from .cache_keys import get_session_key


router = APIRouter(
    tags=["Auth"]
)

async def _create_session_and_set_cookie(
    request: Request,
    response: Response,
    user_id: UUID,
    cache_store: CacheStore
):
    ip = getattr(request.state, "ip", "unknown")
    client_agent = request.headers.get("user-agent", "unknown")

    session_id = await create_session(
        cache_store=cache_store,
        user_id=user_id,
        ip=ip,
        client_agent=client_agent
    )

    response.set_cookie(
        key="session_id",
        value=str(session_id),
        max_age=60*60*24*7, # 7days
        path="/",
        secure=True,
        httponly=True,
        samesite="lax"
    )


@router.post("/email-verification/registration", status_code=200)
async def verify_email_for_registration(
    data: VerifyEmailRequest,
    get_user_by_email_hash: GetUserByEmailHashFn = Depends(provide_get_user_by_email_hash),
    cache_store: CacheStore = Depends(get_cache_store),
    hashing_service: HashingService = Depends(get_hashing_service)
):

    await handle_registration_email_verification(
        email=data.email,
        cache_store=cache_store,
        hashing=hashing_service,
        get_user_by_email_hash=get_user_by_email_hash
    )


    return {"detail": [{"msg": "Verification email sent"}]}


@router.post("", status_code=201, response_model=UserResponse)
async def registration(
    request: Request,
    response: Response,
    data: RegistrationRequest,
    create_user: CreateUserFn = Depends(provide_create_user),
    cache_store: CacheStore = Depends(get_cache_store),
    encryption_service: EncryptionService = Depends(get_encryption_service),
    hashing_service: HashingService = Depends(get_hashing_service)
):
    user =  await handle_registration(
        data=data,
        cache_store=cache_store,
        create_user=create_user,
        encryption=encryption_service,
        hashing=hashing_service
    )

    await _create_session_and_set_cookie(
        request=request,
        response=response,
        user_id=user.id,
        cache_store=cache_store
    )

    return user


@router.post("/login", status_code=200, response_model=UserResponse )
async def login(
    request: Request,
    response: Response,
    data: LoginRequest,
    encryption_service: EncryptionService = Depends(get_encryption_service),
    hashing_service: HashingService = Depends(get_hashing_service),
    cache_store: CacheStore = Depends(get_cache_store),
    get_user_by_email_hash: GetUserByEmailHashFn = Depends(provide_get_user_by_email_hash)
):
    user = await handle_login(
        login_data=data,
        encryption=encryption_service,
        hashing=hashing_service,
        get_user_by_email_hash=get_user_by_email_hash
    )

    await _create_session_and_set_cookie(
        request=request,
        response=response,
        cache_store=cache_store,
        user_id=user.id
    )

    return user


@router.get("/me", status_code=200, response_model=CurrentUserResponse)
async def get_me(
    user: User = Depends(get_current_user)
):
    return handle_get_current_user(user)


@router.post("/logout", status_code=200)
async def logout(
    response: Response,
    session_id: UUID = Depends(get_session_id),
    cache_store: CacheStore = Depends(get_cache_store)
):
    await cache_store.remove(get_session_key(session_id))
    response.delete_cookie(key="session_id", path="/")

    return {"detail": [{"msg": "Logged out"}]}