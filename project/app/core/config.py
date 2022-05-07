from __future__ import annotations

from pathlib import Path
from typing import final

from fastapi.templating import Jinja2Templates
from pydantic import (
    AnyHttpUrl,
    BaseSettings,
    EmailStr,
    HttpUrl,
    PostgresDsn,
    RedisDsn,
    validator,
constr
)


# APPS
# LOGIN URL
# STATIC VALUE

class Settings(BaseSettings):
    @property
    def BASE_DIR(self) -> Path:
        return Path(__file__).parent.parent

    @property
    def TEMPLATE_DIR(self) -> Jinja2Templates:
        return Jinja2Templates(str(self.BASE_DIR / "templates"))

    APP_NAME: str
    APP_DESCRIPTION: str
    API_PREFIX: str = "/api"
    SECRET_KEY: str
    DEBUG: bool = False
    LOGIN_PATH = "/api/auth/login"
    AUTH_TOKEN_LIFETIME_SECONDS = 3600
    SERVER_HOST: AnyHttpUrl
    SENTRY_DSN: HttpUrl | None = None

    REDIS_URL: RedisDsn

    BACKEND_CORS_ORIGINS: list[AnyHttpUrl] = []

    @validator("BACKEND_CORS_ORIGINS", pre=True)
    def assemble_cors_origins(cls, v: str | list[str]) -> list[str] | str:
        if isinstance(v, str) and not v.startswith("["):
            return [i.strip() for i in v.split(",")]
        elif isinstance(v, (list, str)):
            return v
        raise ValueError(v)

    DATABASE_URI: PostgresDsn

    SMTP_TLS: bool = True
    SMTP_PORT: int | None = None
    SMTP_HOST: str | None = None
    SMTP_USER: str | None = None
    SMTP_PASSWORD: str | None = None

    DEFAULT_FROM_EMAIL: EmailStr

    FIRST_SUPERUSER: EmailStr
    FIRST_SUPERUSER_PASSWORD: str

    class Config:
        case_sensitive = True
        env_file = ".env"


settings = Settings()
