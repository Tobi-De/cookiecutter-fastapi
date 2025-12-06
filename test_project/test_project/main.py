import sentry_sdk
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from sentry_sdk.integrations.asgi import SentryAsgiMiddleware
from sentry_sdk.integrations.logging import LoggingIntegration
from sentry_sdk.integrations.redis import RedisIntegration


from .core.auth import get_auth_router
from .core.config import settings, Environment
from .db.config import register_db
from .health import router as health_check_router
from .lifetime import startup
from .users.routes import router as users_router



def get_application() -> FastAPI:
    _app = FastAPI(
        title="Test Project",
        description="",
        debug=settings.DEBUG,
    )
    _app.include_router(get_auth_router())
    _app.include_router(users_router)
    _app.include_router(health_check_router)
    _app.add_middleware(
        CORSMiddleware,
        allow_origins=[str(origin) for origin in settings.BACKEND_CORS_ORIGINS],
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )
    if settings.ENVIRONMENT == Environment.prod:
        assert (
            settings.SENTRY_DSN
        ), "Set SENTRY_DSN to monitor and track errors in production!"
        sentry_sdk.init(
            settings.SENTRY_DSN, integrations=[LoggingIntegration(), RedisIntegration()]
        )
        _app.add_middleware(SentryAsgiMiddleware)
    
    register_db(_app)
    _app.on_event("startup")(startup)

    return _app


app = get_application()
