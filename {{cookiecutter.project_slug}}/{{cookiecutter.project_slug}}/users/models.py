{% if cookiecutter.database == "Tortoise" -%}
from __future__ import annotations

from fastapi_users_tortoise import (
    TortoiseBaseUserAccountModelUUID,
    TortoiseUserDatabase,
)
from tortoise import fields

from {{cookiecutter.project_slug}}.db.models import TimeStampedModel


class User(TortoiseBaseUserAccountModelUUID, TimeStampedModel):
    short_name = fields.CharField(max_length=255, null=True)
    full_name = fields.CharField(max_length=255, null=True)

    class Meta:
        table = "users"

    def __str__(self):
        return self.short_name or self.full_name or self.email


async def get_user_db():
    yield TortoiseUserDatabase(User)
{% endif -%}
{% if cookiecutter.database == "Beanie" -%}
from __future__ import annotations

from beanie import PydanticObjectId
from fastapi_users.db import BeanieBaseUser, BeanieUserDatabase


class User(BeanieBaseUser[PydanticObjectId]):
    short_name: str | None = None
    full_name: str | None = None

    def __str__(self):
        return self.short_name or self.full_name or self.email


async def get_user_db():
    yield BeanieUserDatabase(User)
{% endif -%}