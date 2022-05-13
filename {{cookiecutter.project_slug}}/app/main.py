import sentry_sdk
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from sentry_sdk.integrations.asgi import SentryAsgiMiddleware
from sentry_sdk.integrations.logging import LoggingIntegration
from sentry_sdk.integrations.redis import RedisIntegration

from .core.auth import get_auth_router
from .core.config import settings
from .db.config import register_db
from .lifetime import startup
from .users.routes import router as users_router
from .health import router as health_check_router


def _get_application():
    _app = FastAPI(
        title="{{cookiecutter.project_name}}",
        description="{{cookiecutter.project_description}}",
    )

    # Auth routes
    _app.include_router(get_auth_router())
    _app.include_router(users_router)
    _app.include_router(health_check_router)

    # Middlewares
    _app.add_middleware(
        CORSMiddleware,
        allow_origins=[str(origin) for origin in settings.BACKEND_CORS_ORIGINS],
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )
    {% if cookiecutter.use_sentry == 'y' -%}
    if settings.SENTRY_DSN:
        sentry_sdk.init(
            settings.SENTRY_DSN, integrations=[LoggingIntegration(), RedisIntegration()]
        )
        app.add_middleware(SentryAsgiMiddleware)
    {% endif %}
    # Register tortoise
    register_db(_app)

    # App lifetime
    _app.on_event("startup")(startup)

    return _app


app = _get_application()
