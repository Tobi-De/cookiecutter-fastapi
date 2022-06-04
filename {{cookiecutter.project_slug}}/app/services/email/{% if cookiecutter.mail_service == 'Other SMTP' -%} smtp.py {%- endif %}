from __future__ import annotations

from dataclasses import dataclass
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

from aiosmtplib import SMTP
from aiosmtplib.errors import SMTPException

from app.core.logger import logger
from .errors import SendEmailError


@dataclass
class SMTPMailer:
    host: str
    port: int
    tls: bool
    username: str | None = None
    password: str | None = None

    async def send_email(
        self,
        *,
        recipient: tuple[str, str | None],
        sender: tuple[str, str | None],
        subject: str,
        text: str | None = None,
        html: str | None = None,
    ):
        message = MIMEMultipart("alternative")

        from_email, from_name = sender
        to_email, to_name = recipient
        message["From"] = from_email if not from_name else f"{from_name} <{from_email}>"
        message["To"] = to_email if not from_name else f"{to_name} <{to_email}>"
        message["Subject"] = subject
        if text:
            message.attach(MIMEText(text, "plain", "utf-8"))
        if html:
            message.attach(MIMEText(html, "html", "utf-8"))

        kwargs = {"hostname": self.host, "port": self.port, "use_tls": self.tls}
        if self.username:
            kwargs["username"] = self.username
        if self.password:
            kwargs["password"] = self.password
        smtp_client = SMTP(**kwargs)
        async with smtp_client:
            try:
                response = await smtp_client.send_message(message)
            except SMTPException as e:
                raise SendEmailError(str(e)) from e
        logger.info(f"send email result: {response}")
