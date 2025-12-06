from __future__ import annotations

from uuid import UUID

from fastapi_users import schemas
from pydantic import BaseModel


class BaseUser(BaseModel):
    short_name: str | None = None
    full_name: str | None = None


class UserRead(BaseUser, schemas.BaseUser[UUID]):
    pass


class UserCreate(BaseUser, schemas.BaseUserCreate):
    pass


class UserUpdate(BaseUser, schemas.BaseUserUpdate):
    pass
