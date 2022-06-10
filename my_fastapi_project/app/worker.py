from arq.connections import RedisSettings
from pydantic.utils import import_string
from tortoise import Tortoise

from .core.config import settings
from .db.config import TORTOISE_ORM

ARQ_BACKGROUND_FUNCTIONS = [
    "app.users.tasks.log_user_email",
    "app.services.email.send_email_task",
]
FUNCTIONS = [import_string(bg_func) for bg_func in ARQ_BACKGROUND_FUNCTIONS]


async def startup(_: dict):
    """
    Binds a connection set to the db object.
    """
    await Tortoise.init(config=TORTOISE_ORM)


async def shutdown(_: dict):
    """
    Pops the bind on the db object.
    """
    await Tortoise.close_connections()


class WorkerSettings:
    """
    Settings for the ARQ worker.
    """

    on_startup = startup
    on_shutdown = shutdown
    redis_settings = RedisSettings.from_dsn(dsn=settings.REDIS_URL)
    functions = FUNCTIONS
