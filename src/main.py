from contextlib import asynccontextmanager
from fastapi import FastAPI
from .users.routes import router
from .auth.routes import router as auth_router
from .settings import settings
from .users.sqlalchemy.core import session_maker
from .users.sqlalchemy.middleware import DbSessionMiddleware
from .cryptography.bcrypt.hashing_service import BcryptHashingService
from .cryptography.fernet.encryption_service import EncryptionService
from .cache.redis.cache_store import RedisCacheStore
from .exceptions import ExceptionHanlder


@asynccontextmanager
async def lifespan(app: FastAPI):
    app.state.encryption_service = EncryptionService(settings.ENCRYPTION_KEY)
    app.state.hashing_service = BcryptHashingService()
    app.state.cache_store = RedisCacheStore(settings.REDIS_URL)

    yield

    await app.state.cache_store.close_connection()


app = FastAPI(lifespan=lifespan)


app.add_middleware(ExceptionHanlder)
app.add_middleware(DbSessionMiddleware, session_maker=session_maker)


@app.get("/health")
def health_check():
    return {"detail":[{"msg": "Users service ok"}]}

app.include_router(router, prefix="/api/v1")
app.include_router(auth_router, prefix="/api/v1/auth")

if __name__ == "__main__":
    import uvicorn

    uvicorn.run(
        app="src.main:app",
        host="0.0.0.0",
        port=8000,
        reload=True
    )
