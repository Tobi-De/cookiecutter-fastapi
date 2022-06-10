from __future__ import annotations

import typing
from typing import Protocol, Any

import jinja2

from app.core.config import settings
from .null import Null
from .ses import SES
DEFAULT_SENDER = (settings.DEFAULT_FROM_EMAIL, settings.DEFAULT_FROM_NAME)


class EmailProvider(Protocol):
    async def send_email(
        self,
        *,
        recipient: tuple[str, str | None],
        sender: tuple[str, str | None],
        subject: str,
        text: str | None = None,
        html: str | None = None,
    ):
        ...


@typing.no_type_check
def get_mailer() -> EmailProvider:
    if settings.EMAILS_ENABLED:
        return SES(
            secret_key=settings.SES_SECRET_KEY,
            access_key=settings.SES_ACCESS_KEY,
            region=settings.SES_REGION,
        )
        
    return Null()


def render_email_template(template: str, context: dict[str, Any]) -> str:
    template_object = jinja2.Environment(
        loader=jinja2.FileSystemLoader(settings.PATHS.EMAIL_TEMPLATES_DIR),
        autoescape=True,
    ).get_template(template)
    return template_object.render(context)


async def send_email_task(
    _: dict,
    *,
    recipient: tuple[str, str | None],
    sender: tuple[str, str | None] = DEFAULT_SENDER,
    subject: str,
    text: str | None = None,
    html: str | None = None,
):
    await mailer.send_email(
        recipient=recipient, sender=sender, subject=subject, text=text, html=html
    )


mailer = get_mailer()
