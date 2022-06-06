from __future__ import annotations

from dataclasses import dataclass, field

from aioaws.ses import SesConfig, SesClient, SesRecipient
from httpx import AsyncClient, RequestError

from app.core.logger import logger
from .errors import SendEmailError


@dataclass
class SES:
    access_key: str
    secret_key: str
    region: str
    _client: SesClient = field(init=False)

    def __post_init__(self):
        self._client = SesClient(
            AsyncClient(), SesConfig(self.access_key, self.secret_key, self.region)
        )

    async def send_email(
            self,
            *,
            recipient: tuple[str, str | None],
            sender: tuple[str, str | None],
            subject: str,
            text: str | None = None,
            html: str | None = None,
    ):
        from_email, from_name = sender
        to_email, to_name = recipient
        text_body = text or ""
        try:
            message_id = await self._client.send_email(
                e_from=SesRecipient(from_email, from_name),
                subject=subject,
                to=[SesRecipient(to_email, to_name)],
                text_body=text_body,
                html_body=html,
            )
            logger.info(f"SES message ID: {message_id}")
        except RequestError as e:
            raise SendEmailError(str(e)) from e
