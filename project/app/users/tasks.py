from app.logger import logger
from app.procrastinate import app


@app.task()
async def log_user_email(user_email: str) -> None:
    logger.info(f"User email: {user_email}")
