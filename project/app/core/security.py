from fastapi_users import FastAPIUsers
from fastapi_users.authentication import (
    AuthenticationBackend,
    BearerTransport,
    CookieTransport,
    JWTStrategy,
)

from app.users.schemas import UserRead, UserCreate, UserInDB, UserUpdate
from app.users.manager import get_user_manager
from .config import settings

bearer_transport = BearerTransport(tokenUrl=settings.LOGIN_PATH)
cookie_transport = CookieTransport(cookie_max_age=settings.AUTH_TOKEN_LIFETIME_SECONDS)


def get_jwt_strategy() -> JWTStrategy:
    return JWTStrategy(
        secret=settings.SECRET_KEY,
        lifetime_seconds=settings.AUTH_TOKEN_LIFETIME_SECONDS,
    )


bearer_auth_backend = AuthenticationBackend(
    name="jwt",
    transport=bearer_transport,
    get_strategy=get_jwt_strategy,
)
cookie_auth_backend = AuthenticationBackend(
    name="cookie", transport=cookie_transport, get_strategy=get_jwt_strategy
)

fastapi_users = FastAPIUsers(
    get_user_manager,
    [bearer_auth_backend, cookie_auth_backend],
    UserRead,
    UserCreate,
    UserUpdate,
    UserInDB,
)
