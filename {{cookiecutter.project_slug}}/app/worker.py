from arq.connections import RedisSettings
from pydantic.utils import import_string
{% if cookiecutter.database == "Tortoise" -%}
from tortoise import Tortoise
{% endif %}

from .core.config import settings
{% if cookiecutter.database == "Tortoise" -%}
from .db.config import TORTOISE_ORM
{% endif %}
{% if cookiecutter.database == "Beanie" -%}
from .db.config import init_db
{% endif %}

ARQ_BACKGROUND_FUNCTIONS = [
    "app.users.tasks.log_user_email",
    "app.services.email.send_email_task",
]
FUNCTIONS = [import_string(bg_func) for bg_func in ARQ_BACKGROUND_FUNCTIONS]


async def startup(_: dict):
    """
    Binds a connection set to the db object.
    """
    {% if cookiecutter.database == "Tortoise" -%}
    await Tortoise.init(config=TORTOISE_ORM)
    {% endif %}
    {% if cookiecutter.database == "Beanie" -%}
    await init_db()
    {% endif %}

{% if cookiecutter.database == "Tortoise" -%}
async def shutdown(_: dict):
    """
    Pops the bind on the db object.
    """
    await Tortoise.close_connections()
{% endif %}

class WorkerSettings:
    """
    Settings for the ARQ worker.
    """

    on_startup = startup
    {% if cookiecutter.database == "Tortoise" -%}
    on_shutdown = shutdown
    {% endif -%}
    redis_settings = RedisSettings.from_dsn(dsn=settings.REDIS_URL)
    functions = FUNCTIONS
