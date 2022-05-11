from email.message import EmailMessage

from aiosmtplib import SMTP
from arq import create_pool
from arq.connections import RedisSettings

from app.core.config import settings
from app.logger import logger


async def enqueue_job(func: str, *args, **kwargs) -> None:
    redis = await create_pool(RedisSettings.from_dsn(dsn=settings.REDIS_URL))
    await redis.enqueue_job(func, *args, **kwargs)


# TODO this should probably be made a background task, it really slows api responses.
async def send_email(email_to: str, subject: str = "", body: str = "") -> None:
    assert settings.EMAILS_ENABLED, "no provided configuration for email variables"
    message = EmailMessage()
    message["From"] = settings.DEFAULT_FROM_EMAIL
    message["To"] = email_to
    message["Subject"] = subject
    message.set_content(body)

    auth = {}
    if settings.SMTP_USER:
        auth["username"] = settings.SMTP_USER
    if settings.SMTP_PASSWORD:
        auth["password"] = settings.SMTP_PASSWORD
    smtp_client = SMTP(
        hostname=settings.SMTP_HOST,
        port=settings.SMTP_PORT,
        use_tls=settings.SMTP_TLS,
        **auth,
    )
    async with smtp_client:
        response = await smtp_client.send_message(message)
    logger.info(f"send email result: {response}")
