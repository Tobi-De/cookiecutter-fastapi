from fastapi import APIRouter, Depends
from app.core.pagination import Page, Params, paginate

from app.core.auth import fastapi_users
from app.worker import queue

from app.core.auth import current_user
from .models import User
from .schemas import UserRead, UserUpdate

router = APIRouter(prefix="/users", tags=["users"])


@router.get("/", response_model=Page[UserRead], dependencies=[Depends(current_user)])
async def user_list(params: Params = Depends()):
    {% if cookiecutter.database == "Tortoise" -%}
    return await paginate(User.all(), params)
    {% endif %}
    {% if cookiecutter.database == "Beanie" -%}
    return await paginate(User.all().sort(User.email), params)
    {% endif %}

@router.get("/log-user-info")
async def log_user_info(user: User = Depends(current_user)):
    await queue.enqueue("log_user_email", user_email=user.email)


router.include_router(fastapi_users.get_users_router(UserRead, UserUpdate))
