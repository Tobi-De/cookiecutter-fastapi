from fastapi import FastAPI
from starlette.staticfiles import StaticFiles

from {{cookiecutter.project_slug}}.core.auth import fastapi_users, frontend_auth_backend
from {{cookiecutter.project_slug}}.core.config import settings
from .routers.home import router as home_router


def get_application() -> FastAPI:
    _app = FastAPI(
        title="Frontend", include_in_schema=False, docs_url=None, redoc_url=None
    )

    _app.include_router(
        fastapi_users.get_auth_router(frontend_auth_backend),
        prefix="/auth",
    )
    _app.include_router(home_router)

    _app.mount(
        "/static", StaticFiles(directory=settings.PATHS.STATIC_FILES_DIR), name="static"
    )
    return _app


app = get_application()
