from __future__ import annotations

from typing import Generic, TypeVar

from pydantic import BaseModel, Field
from pydantic.generics import GenericModel
{% if cookiecutter.database == "Beanie" -%}
from beanie.odm.queries.find import FindMany
{% endif -%}
{% if cookiecutter.database == "Tortoise" -%}
from tortoise.queryset import QuerySet
{% endif -%}

from .config import settings

T = TypeVar("T", bound=BaseModel)


class Params(BaseModel):
    limit: int = Field(settings.PAGINATION_PER_PAGE, gt=0)
    offset: int = Field(0, gt=-1)


class Page(GenericModel, Generic[T]):
    items: list[T]
    total: int

{% if cookiecutter.database == "Tortoise" -%}
async def paginate(items: QuerySet, params: Params) -> dict:
    offset = params.offset
    limit = params.limit
    return {
        "items": await items.limit(limit).offset(offset).order_by("-created_at"),
        "total": await items.count(),
    }
{% endif -%}
{% if cookiecutter.database == "Beanie" -%}
async def paginate(items: FindMany, params: Params) -> dict:
    offset = params.offset
    limit = params.limit
    return {
        "items": await items.limit(limit).skip(offset).to_list(),
        "total": await items.count(),
    }
{% endif -%}
