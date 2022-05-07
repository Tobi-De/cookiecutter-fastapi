from __future__ import annotations

from typing import cast

from arq import create_pool
from arq.connections import RedisSettings
from fastapi import Request
from fastapi.responses import HTMLResponse

from app.core.config import settings


def render_html(
    request: Request, template_name: str, context: dict | None = None
) -> HTMLResponse:
    context = context or {}
    return cast(
        HTMLResponse,
        settings.TEMPLATE_DIR.TemplateResponse(
            template_name, {"request": request, **context}
        ),
    )


async def enqueue_job(func: callable, *args, **kwargs) -> None:
    redis = await create_pool(RedisSettings.from_dsn(dsn=settings.REDIS_URL))
    await redis.enqueue_job(func, *args, **kwargs)
