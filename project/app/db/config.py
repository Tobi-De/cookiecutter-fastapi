from fastapi import FastAPI
from tortoise.contrib.fastapi import register_tortoise

from app.core.config import settings

TORTOISE_ORM = {
    "connections": {"default": settings.DATABASE_URI},
    "apps": {
        "models": {
            "models": ["app.users.models", "aerich.models"],
            "default_connection": "default",
        },
    },
}


def register_db(app: FastAPI) -> None:
    register_tortoise(
        app,
        db_url=settings.DATABASE_URI,
        modules={"models": ["app.users.models"]},
        generate_schemas=False,
        add_exception_handlers=True,
    )
