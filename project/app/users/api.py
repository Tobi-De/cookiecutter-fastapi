from fastapi import APIRouter, Depends

from app.core.auth import fastapi_users
from .deps import current_user
from .models import User
from .schemas import UserRead, UserUpdate

router = APIRouter(prefix="/users", tags=["users"])
router.include_router(fastapi_users.get_users_router(UserRead, UserUpdate))


@router.get("/log-user-info")
def log_user_info(user: User = Depends(current_user)):
    pass
