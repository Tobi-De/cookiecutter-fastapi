from fastapi_users.exceptions import UserAlreadyExists

from .core.config import settings
from app.core.logger import logger
from .users.schemas import UserCreate
from .users.utils import create_user


async def create_superuser() -> None:
    try:
        user = await create_user(
            UserCreate(
                email=settings.FIRST_SUPERUSER_EMAIL,
                password=settings.FIRST_SUPERUSER_PASSWORD,
                is_superuser=True,
                is_verified=True,
                is_active=True,
            )
        )
        logger.info(f"User {user} created")
    except UserAlreadyExists:
        logger.info(f"User {settings.FIRST_SUPERUSER_EMAIL} already exists")
