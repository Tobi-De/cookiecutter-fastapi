from fastapi import Depends
from fastapi_users import BaseUserManager, InvalidPasswordException
from fastapi_users.db import TortoiseUserDatabase

from app.core.config import settings
from .models import User
from .schemas import UserCreate, UserInDB


class UserManager(BaseUserManager[UserCreate, UserInDB]):
    user_db_model = UserInDB
    reset_password_token_secret = settings.SECRET_KEY
    verification_token_secret = settings.SECRET_KEY

    async def validate_password(self, password: str, user: UserInDB) -> None:
        conditions = {
            "Password should be at least 8 characters": len(password) < 8,
            "Password should not contain e-mail": user.email in password,
            "Password should contain at least one number or special characters(@#*)": password.isalpha(),
            "Password should not contain only numeric values": password.isnumeric(),
        }
        for msg, condition in conditions.items():
            if condition:
                raise InvalidPasswordException(msg)


async def get_user_db():
    yield TortoiseUserDatabase(UserInDB, User)


async def get_user_manager(user_db: TortoiseUserDatabase = Depends(get_user_db)):
    yield UserManager(user_db)
