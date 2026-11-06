import uuid
from datetime import datetime, timezone
from sqlmodel import Field, SQLModel


class UserBase(SQLModel):
    """Shared properties between API schemas and database model."""
    email: str = Field(unique=True, index=True, max_length=255)
    is_active: bool = Field(default=True)
    is_superuser: bool = Field(default=False)


class User(UserBase, table=True):
    """Database table model."""
    __tablename__ = "users"

    id: uuid.UUID = Field(default_factory=uuid.uuid4, primary_key=True)
    hashed_password: str
    created_at: datetime = Field(
        default_factory=lambda: datetime.now(timezone.utc),
        nullable=False,
    )
    updated_at: datetime = Field(
        default_factory=lambda: datetime.now(timezone.utc),
        nullable=False,
    )


# --- DTOs / Schemas for Auth and API ---

class UserCreate(UserBase):
    """Payload for user registration."""
    password: str = Field(min_length=8, max_length=128)


class UserLogin(SQLModel):
    """Payload for JSON user login."""
    email: str
    password: str


class UserRead(UserBase):
    """Payload returned in responses (excludes hashed_password)."""
    id: uuid.UUID
    created_at: datetime
