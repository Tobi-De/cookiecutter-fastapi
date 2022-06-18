from __future__ import annotations
{% if cookiecutter.database == "Tortoise" -%}
from uuid import UUID
{% endif -%}
{% if cookiecutter.database == "Beanie" -%}
from beanie import PydanticObjectId
{% endif -%}
from fastapi import Depends, Request
from fastapi_users import BaseUserManager, InvalidPasswordException, UUIDIDMixin
{% if cookiecutter.database == "Tortoise" -%}
from fastapi_users_tortoise import TortoiseUserDatabase
{% endif -%}
{% if cookiecutter.database == "Beanie" -%}
from fastapi_users.db import BeanieUserDatabase, ObjectIDIDMixin
{% endif -%}
from app.core.config import settings
from app.services.email import render_email_template
from app.utils import enqueue_job
from .models import User, get_user_db

{% if cookiecutter.database == "Tortoise" -%}
class UserManager(UUIDIDMixin, BaseUserManager[User, UUID]):
{% endif %}
{% if cookiecutter.database == "Beanie" -%}
class UserManager(UUIDIDMixin, BaseUserManager[User, PydanticObjectId]):
{% endif %}

    reset_password_token_secret = settings.SECRET_KEY
    verification_token_secret = settings.SECRET_KEY

    async def on_after_register(
        self, user: User, request: Request | None = None
    ) -> None:
        name = user.full_name or user.short_name
        subject = f"Welcome to {name}!" if name else "Welcome!"
        await enqueue_job(
            "send_email_task",
            recipient=(user.email, None),
            subject=subject,
            html=render_email_template("welcome.html", context={"user": user}),
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

{% if cookiecutter.database == "Tortoise" -%}
async def get_user_manager(user_db: TortoiseUserDatabase = Depends(get_user_db)):
    yield UserManager(user_db)
{% endif -%}
{% if cookiecutter.database == "Beanie" -%}
async def get_user_manager(user_db: BeanieUserDatabase = Depends(get_user_db)):
    yield UserManager(user_db)
{% endif -%}
