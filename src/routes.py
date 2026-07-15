from fastapi import APIRouter
from .schemas import UserResponse

router = APIRouter(
    tags=["Users"]
)

@router.post("", status_code=201)
async def users_create():
    pass

@router.delete("/{user_id}", status_code=200)
async def users_delete():
    pass