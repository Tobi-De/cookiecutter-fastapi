import uuid

from fastapi import APIRouter
from fastapi_users import FastAPIUsers
from fastapi_users.authentication import (
    AuthenticationBackend,
    BearerTransport,
    CookieTransport,
    JWTStrategy,
)

from app.users.manager import get_user_manager
from app.users.models import User
from app.users.schemas import UserCreate, UserRead

from .config import settings

bearer_transport = BearerTransport(tokenUrl=settings.LOGIN_PATH)
cookie_transport = CookieTransport(cookie_max_age=settings.AUTH_TOKEN_LIFETIME_SECONDS)


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

fastapi_users = FastAPIUsers[User, uuid.UUID](get_user_manager, [auth_backend])


def get_auth_router() -> APIRouter:
    router = APIRouter(prefix="/auth", tags=["auth"])

    router.include_router(fastapi_users.get_auth_router(auth_backend))
    router.include_router(fastapi_users.get_register_router(UserRead, UserCreate))
    router.include_router(fastapi_users.get_reset_password_router())
    router.include_router(fastapi_users.get_verify_router(UserRead))
    return router
