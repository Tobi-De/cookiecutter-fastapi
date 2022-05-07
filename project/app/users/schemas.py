from __future__ import annotations

from fastapi_users import models
from tortoise.contrib.pydantic import PydanticModel

from .models import User


class UserRead(models.BaseUser):
    short_name: str | None = None
    full_name: str | None = None


class UserCreate(UserRead, models.BaseUserCreate):
    pass


class UserUpdate(UserRead, models.BaseUserUpdate):
    pass


class UserInDB(UserRead, models.BaseUserDB, PydanticModel):
    class Config:
        orm_mode = True
        orig_model = User
