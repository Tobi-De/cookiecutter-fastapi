from arq import create_pool
from arq.connections import RedisSettings

from app.core.config import settings


async def enqueue_job(func: str, *args, **kwargs) -> None:
    redis = await create_pool(RedisSettings.from_dsn(dsn=settings.REDIS_URL))
    await redis.enqueue_job(func, *args, **kwargs)
