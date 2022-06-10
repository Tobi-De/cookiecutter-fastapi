from app.core.logger import logger


async def log_user_email(_: dict, user_email: str) -> None:
    logger.info(f"User email: {user_email}")
