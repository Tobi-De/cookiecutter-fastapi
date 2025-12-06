{% if cookiecutter.database == "Beanie" -%}
from beanie import PydanticObjectId
{% endif -%}
{% if cookiecutter.database == "Tortoise" -%}
import uuid
{% endif -%}

from fastapi import APIRouter
from fastapi_users import FastAPIUsers
from fastapi_users.authentication import (
    AuthenticationBackend,
    BearerTransport,
    CookieTransport,
    JWTStrategy,
)

from {{cookiecutter.project_slug}}.users.manager import get_user_manager
from {{cookiecutter.project_slug}}.users.models import User
from {{cookiecutter.project_slug}}.users.schemas import UserCreate, UserRead
from .config import settings

bearer_transport = BearerTransport(tokenUrl=settings.PATHS.LOGIN_PATH)
{% if cookiecutter.render_html != 'n' -%}
cookie_transport = CookieTransport(cookie_max_age=settings.AUTH_TOKEN_LIFETIME_SECONDS)
{% endif %}

def get_jwt_strategy() -> JWTStrategy:
    return JWTStrategy(
        secret=settings.SECRET_KEY,
        lifetime_seconds=settings.AUTH_TOKEN_LIFETIME_SECONDS,
    )


auth_backend = AuthenticationBackend(
    name="jwt",
    transport=bearer_transport,
    get_strategy=get_jwt_strategy,
)
{% if cookiecutter.render_html != 'n' -%}
frontend_auth_backend = AuthenticationBackend(
    name="cookie", transport=cookie_transport, get_strategy=get_jwt_strategy
)
{% endif %}

{%- if cookiecutter.render_html == 'n' and cookiecutter.database == "Tortoise" %}
fastapi_users = FastAPIUsers[User, uuid.UUID](get_user_manager, [auth_backend])
{% endif %}
{% if cookiecutter.render_html != 'n'  and cookiecutter.database == "Tortoise" %}
fastapi_users = FastAPIUsers[User, uuid.UUID](
    get_user_manager, [auth_backend, frontend_auth_backend]
)
{% endif %}

{%- if cookiecutter.render_html == 'n' and cookiecutter.database == "Beanie" %}
fastapi_users = FastAPIUsers[User, PydanticObjectId](get_user_manager, [auth_backend])
{% endif %}
{% if cookiecutter.render_html != 'n' and cookiecutter.database == "Beanie" %}
fastapi_users = FastAPIUsers[User, PydanticObjectId](
    get_user_manager, [auth_backend, frontend_auth_backend]
)
{% endif %}

def get_auth_router() -> APIRouter:
    router = APIRouter(prefix="/auth", tags=["auth"])

    router.include_router(fastapi_users.get_auth_router(auth_backend))
    router.include_router(fastapi_users.get_register_router(UserRead, UserCreate))
    router.include_router(fastapi_users.get_reset_password_router())
    router.include_router(fastapi_users.get_verify_router(UserRead))
    return router


current_user = fastapi_users.current_user(active=True)
superuser = fastapi_users.current_user(active=True, superuser=True)
