from fastapi import APIRouter, Depends
from fastapi_pagination import Page, Params
from fastapi_pagination.ext.tortoise import paginate

from app.core.auth import fastapi_users
from app.utils import enqueue_job

from .deps import current_user
from .models import User
from .schemas import UserRead, UserUpdate

router = APIRouter(prefix="/users", tags=["users"])


@router.get("/", response_model=Page[UserRead], dependencies=[Depends(current_user)])
async def user_list(params: Params = Depends()):
    return paginate(User.all(), params)


@router.get("/log-user-info")
async def log_user_info(user: User = Depends(current_user)):
    await enqueue_job("log_user_email", user_email=user.email)


router.include_router(fastapi_users.get_users_router(UserRead, UserUpdate))
