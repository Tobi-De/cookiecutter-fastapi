from __future__ import annotations

from uuid import UUID

from fastapi import Depends, Request
from fastapi_users import BaseUserManager, InvalidPasswordException, UUIDIDMixin
from fastapi_users_tortoise import TortoiseUserDatabase

from app.core.config import settings
from app.utils import send_email

from .models import User, get_user_db


class UserManager(UUIDIDMixin, BaseUserManager[User, UUID]):
    reset_password_token_secret = settings.SECRET_KEY
    verification_token_secret = settings.SECRET_KEY

    async def on_after_register(
        self, user: User, request: Request | None = None
    ) -> None:
        await send_email(
            email_to=user.email, subject="Welcome!", body=f"Welcome to {user}"
        )

    async def validate_password(self, password: str, user: User) -> None:
        conditions = {
            "Password should be at least 8 characters": len(password) < 8,
            "Password should not contain e-mail": user.email in password,
            "Password should contain at least one number or special characters(@#*)": password.isalpha(),
            "Password should not contain only numeric values": password.isnumeric(),
        }
        for msg, condition in conditions.items():
            if condition:
                raise InvalidPasswordException(msg)


async def get_user_manager(user_db: TortoiseUserDatabase = Depends(get_user_db)):
    yield UserManager(user_db)
