from pydantic import BaseModel, ConfigDict
from uuid import UUID
from datetime import datetime


class ApiSchema(BaseModel):
    model_config = ConfigDict(str_strip_whitespace=True)


class UserCreateRequest(BaseModel):
    email: str
    password: str


class UserResponse(BaseModel):
    id: UUID
    email: str
    created_at: datetime