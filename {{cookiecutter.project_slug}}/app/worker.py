from saq import Queue
from importlib import import_module
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

BACKGROUND_FUNCTIONS = [
    "app.users.tasks.log_user_email",
    "app.services.email.send_email_task",
]


def import_string(dotted_path: str):
    """
    Import a module, or resolve an attribute of a module.
    """
    try:
        module_path, class_name = dotted_path.rsplit(".", 1)
    except ValueError as err:
        raise ImportError(f"{dotted_path} doesn't look like a module path") from err

    module = import_module(module_path)
    try:
        return getattr(module, class_name)
    except AttributeError as err:
        raise ImportError(
            f"Module '{module_path}' does not have attribute '{class_name}'"
        ) from err


FUNCTIONS = [import_string(bg_func) for bg_func in BACKGROUND_FUNCTIONS]


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

queue = Queue.from_url(settings.REDIS_URL)

settings = {
    "queue": queue,
    "functions": FUNCTIONS,
    "concurrency": 10,
    "startup": startup,
    "shutdown": shutdown,
}

