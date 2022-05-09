from fastapi_mail import FastMail, ConnectionConfig
from fastapi_mail import MessageSchema  # noqa

from .config import settings

mail = FastMail(
    ConnectionConfig(
        MAIL_USERNAME=settings.SMTP_USER,
        MAIL_PASSWORD=settings.SMTP_PASSWORD,
        MAIL_FROM=settings.DEFAULT_FROM_EMAIL,
        MAIL_PORT=settings.SMTP_PORT,
        MAIL_SERVER=settings.SMTP_HOST,
        # MAIL_TLS=settings.SMTP_TLS,
        MAIL_SSL=False,
    )
)
