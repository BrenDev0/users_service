from sqlalchemy.ext.asyncio import AsyncSession
from ..models import User, UserCreate
from .models import UserRow
from .mappers import domain_create_to_row, row_to_domain

async def create(db: AsyncSession, domain_create: UserCreate) -> User:
    row = domain_create_to_row(domain_create=domain_create)
    db.add(row)
    await db.flush()
    await db.refresh(row)

    return row_to_domain(row)