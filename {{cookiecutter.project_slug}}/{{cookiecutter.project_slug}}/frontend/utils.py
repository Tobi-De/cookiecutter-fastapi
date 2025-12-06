from __future__ import annotations

from typing import cast, Mapping

from fastapi import Request
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from starlette.background import BackgroundTask

from {{cookiecutter.project_slug}}.core.config import settings


def render_html(
    request: Request,
    template_name: str,
    context: dict | None = None,
    status_code: int = 200,
    headers: Mapping[str, str] | None = None,
    media_type: str | None = None,
    background: BackgroundTask | None = None,
) -> HTMLResponse:
    template_object = Jinja2Templates(directory=settings.PATHS.TEMPLATES_DIR)
    context = context or {}
    return cast(
        HTMLResponse,
        template_object.TemplateResponse(
            name=template_name,
            context={"request": request, **context},
            status_code=status_code,
            headers=headers,
            media_type=media_type,
            background=background,
        ),
    )
