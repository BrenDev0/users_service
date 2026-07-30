from uuid import UUID
from typing import Callable, Awaitable
from .models import User, UserCreate


CreateUserFn = Callable[[UserCreate], Awaitable[User | None]]
GetUserByIdFn = Callable[[UUID], Awaitable[User | None]]
GetUserByEmailHashFn = Callable[[str], Awaitable[User | None]]
DeleteUserByIdFn = Callable[[UUID], Awaitable[bool]]