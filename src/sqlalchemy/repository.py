from uuid import UUID
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, delete
from ..models import User, UserCreate
from .models import UserRow
from .mappers import domain_create_to_row, row_to_domain

async def create(db: AsyncSession, domain_create: UserCreate) -> User:
    row = domain_create_to_row(domain_create=domain_create)
    db.add(row)
    await db.flush()
    await db.refresh(row)

    return row_to_domain(row)

async def get_by_id(db: AsyncSession, user_id: UUID) -> User | None:
    stmt = select(UserRow).where(UserRow.id == user_id)

    result = await db.execute(stmt)
    row = result.scalar_one_or_none()

    return row_to_domain(row) if row else None

async def delete_by_id(db: AsyncSession, user_id: UUID) -> User | None:
    stmt = delete(UserRow).where(UserRow.id == user_id).returning(UserRow)

    result = await db.execute(stmt)

    row = result.scalar_one_or_none()
    return row_to_domain(row) if row else None