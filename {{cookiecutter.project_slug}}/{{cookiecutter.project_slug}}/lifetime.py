from {{cookiecutter.project_slug}}.initial_data import create_superuser
{% if cookiecutter.database == "Beanie" -%}
from .db.config import init_db
{% endif %}


async def startup() -> None:
    {% if cookiecutter.database == "Beanie" -%}
    await init_db()
    {% endif -%}
    await create_superuser()
