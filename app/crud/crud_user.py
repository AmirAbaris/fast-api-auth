import uuid
from sqlmodel import select
from sqlmodel.ext.asyncio.session import AsyncSession

from app.core.security import get_password_hash, verify_password
from app.models.user import User, UserCreate


async def get_user_by_email(db: AsyncSession, email: str) -> User | None:
    """Query user by email."""
    result = await db.exec(select(User).where(User.email == email))
    return result.first()


async def get_user_by_id(db: AsyncSession, user_id: uuid.UUID) -> User | None:
    """Query user by id."""
    result = await db.exec(select(User).where(User.id == user_id))
    return result.first()


async def create_user(db: AsyncSession, user_in: UserCreate) -> User:
    """Create a new user with hashed password."""
    db_user = User(
        email=user_in.email,
        hashed_password=get_password_hash(user_in.password),
        is_active=user_in.is_active,
        is_superuser=user_in.is_superuser,
    )
    db.add(db_user)
    await db.commit()
    await db.refresh(db_user)
    return db_user


async def authenticate_user(
    db: AsyncSession,
    email: str,
    password: str,
) -> User | None:
    """Authenticate user credentials."""
    user = await get_user_by_email(db, email=email)
    if not user:
        return None
    if not verify_password(password, user.hashed_password):
        return None
    return user
