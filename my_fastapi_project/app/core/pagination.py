from __future__ import annotations

from typing import Generic, TypeVar

from pydantic import BaseModel, Field
from pydantic.generics import GenericModel
from tortoise.queryset import QuerySet

from .config import settings

T = TypeVar("T", bound=BaseModel)


class Params(BaseModel):
    limit: int = Field(settings.PAGINATION_PER_PAGE, gt=0)
    offset: int = Field(0, gt=-1)


class Page(GenericModel, Generic[T]):
    items: list[T]
    total: int


async def paginate(items: QuerySet, params: Params) -> dict:
    offset = params.offset
    limit = params.limit
    return {
        "items": await items.limit(limit).offset(offset).order_by("-created_at"),
        "total": await items.count(),
    }
