from __future__ import annotations

from fastapi_users.db import TortoiseBaseUserModel
from tortoise import fields

from app.db.models import TimeStampedModel


class User(TortoiseBaseUserModel, TimeStampedModel):
    short_name = fields.CharField(max_length=255, null=True)
    full_name = fields.CharField(max_length=255, null=True)

    class Meta:
        table = "users"
