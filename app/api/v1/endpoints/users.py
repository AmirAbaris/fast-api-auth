from fastapi import APIRouter

from app.api.deps import CurrentUserDep
from app.models.user import UserRead

router = APIRouter(prefix="/users", tags=["users"])


@router.get("/me", response_model=UserRead)
async def read_current_user(current_user: CurrentUserDep) -> UserRead:
    """Get profile information for the authenticated user."""
    return current_user
