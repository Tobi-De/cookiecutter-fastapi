from fastapi_users.manager import UserAlreadyExists

from .core.config import settings
from .logger import logger
from .users.schemas import UserCreate
from .users.utils import create_user


async def create_superuser() -> None:
    try:
        user = await create_user(
            UserCreate(
                email=settings.FIRST_SUPERUSER,
                password=settings.FIRST_SUPERUSER_PASSWORD,
                is_superuser=True,
                is_verified=True,
                is_active=True,
            )
        )
        logger.info(f"User {user.email} created")
    except UserAlreadyExists:
        logger.info(f"User {settings.FIRST_SUPERUSER} already exists")
