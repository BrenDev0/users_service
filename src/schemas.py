from pydantic import BaseModel
from uuid import UUID
from datetime import datetime


class UserCreateRequest(BaseModel):
    email: str
    password: str


class UserResponse(BaseModel):
    id: UUID
    email: str
    created_at: datetime