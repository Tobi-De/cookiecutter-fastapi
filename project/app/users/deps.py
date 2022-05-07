from fastapi import Depends

from app.core.security import fastapi_users
from .models import User
from .schemas import UserInDB


# Use directly fastapi_users dependencies if you are fine with just getting
# a pydantic model


async def current_user(
    user: UserInDB = Depends(fastapi_users.current_user(active=True)),
) -> User:
    # Get the database user object, use
    return await User.get(id=user.id)


async def superuser(
    user: UserInDB = Depends(fastapi_users.current_user(active=True, superuser=True))
) -> User:
    # Get the database superuser object
    return await User.get(id=user.id)
