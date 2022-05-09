from __future__ import annotations

from pathlib import Path

from pydantic import (
    AnyHttpUrl,
    BaseSettings,
    EmailStr,
    HttpUrl,
    PostgresDsn,
    RedisDsn,
    validator,
)


# APPS


class Settings(BaseSettings):
    # project/app
    BASE_DIR: Path = Path(__file__).parent.parent

    APP_NAME: str
    APP_DESCRIPTION: str
    SECRET_KEY: str
    DEBUG: bool = False
    LOGIN_PATH = "/auth/login"
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
    SMTP_PORT: int = 8025
    SMTP_HOST: str = "localhost"
    SMTP_USER: str = ""
    SMTP_PASSWORD: str = ""

    DEFAULT_FROM_EMAIL: EmailStr

    FIRST_SUPERUSER: EmailStr
    FIRST_SUPERUSER_PASSWORD: str

    class Config:
        case_sensitive = True
        env_file = ".env"


settings = Settings()
