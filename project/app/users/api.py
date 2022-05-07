from fastapi import APIRouter

from app.core.security import bearer_auth_backend, fastapi_users

router = APIRouter(prefix="/users")

router.include_router(
    fastapi_users.get_auth_router(bearer_auth_backend), prefix="/auth", tags=["auth"]
)
router.include_router(
    fastapi_users.get_register_router(), prefix="/auth", tags=["auth"]
)
router.include_router(
    fastapi_users.get_reset_password_router(),
    prefix="/auth",
    tags=["auth"],
)
router.include_router(
    fastapi_users.get_verify_router(),
    prefix="/auth",
    tags=["auth"],
)
router.include_router(fastapi_users.get_users_router(), prefix="/users", tags=["users"])
