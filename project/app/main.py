import sentry_sdk
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from sentry_sdk.integrations.asgi import SentryAsgiMiddleware
from sentry_sdk.integrations.logging import LoggingIntegration
from sentry_sdk.integrations.redis import RedisIntegration

from .core.config import settings
from .db.config import register_db
from .lifetime import startup
from .users.api import router as users_router
from .views.router import router as views_router


def _get_application():
    _app = FastAPI(title=settings.APP_NAME, description=settings.APP_DESCRIPTION)

    # Routes
    _app.include_router(users_router)
    _app.include_router(views_router, include_in_schema=False)

    # Middlewares
    _app.add_middleware(
        CORSMiddleware,
        allow_origins=[str(origin) for origin in settings.BACKEND_CORS_ORIGINS],
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )

    if settings.SENTRY_DSN:
        sentry_sdk.init(
            settings.SENTRY_DSN, integrations=[LoggingIntegration(), RedisIntegration()]
        )
        app.add_middleware(SentryAsgiMiddleware)

    # Register tortoise
    register_db(_app)

    # App lifetime
    _app.on_event("startup")(startup)

    # StaticFiles
    _app.mount(
        "/static",
        StaticFiles(directory=str(settings.BASE_DIR / "static")),
        name="static",
    )

    return _app


app = _get_application()
