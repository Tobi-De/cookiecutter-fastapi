from __future__ import annotations

from pathlib import Path
from typing import Any

from pydantic import (
    AnyHttpUrl,
    EmailStr,
    HttpUrl,
    {% if cookiecutter.database == "Tortoise" -%}
    PostgresDsn,
    {% endif -%}
    {% if cookiecutter.database == "Beanie" -%}
    AnyUrl,
    {% endif -%}
    RedisDsn,
    field_validator,
)
from pydantic_core import ValidationInfo
from pydantic_settings import BaseSettings, SettingsConfigDict

try:
    from enum import StrEnum
except ImportError:
    from enum import Enum

    class StrEnum(str, Enum):
        pass


class Environment(StrEnum):
    dev = "dev"
    prod = "prod"

class Paths:
    # {{cookiecutter.project_slug}}
    ROOT_DIR: Path = Path(__file__).parent.parent.parent
    BASE_DIR: Path = ROOT_DIR / "{{cookiecutter.project_slug}}"
    {% if cookiecutter.render_html != 'n' -%}
    TEMPLATES_DIR: Path = BASE_DIR / "templates"
    STATIC_FILES_DIR: Path = BASE_DIR / "static"
    {% endif -%}
    EMAIL_TEMPLATES_DIR: Path = BASE_DIR / "emails"
    LOGIN_PATH: str = "/auth/login"


class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_file=".env")

    @property
    def PATHS(self) -> Paths:
        return Paths()

    ENVIRONMENT: Environment = "dev"
    SECRET_KEY: str
    DEBUG: bool = False
    AUTH_TOKEN_LIFETIME_SECONDS = 3600
    SERVER_HOST: AnyHttpUrl = "http://localhost:8000"  # type:ignore
    {% if cookiecutter.use_sentry == 'y' -%}
    SENTRY_DSN: HttpUrl | None = None
    {% endif -%}
    PAGINATION_PER_PAGE: int = 20

    REDIS_URL: RedisDsn

    BACKEND_CORS_ORIGINS: list[AnyHttpUrl] = []

    @field_validator("BACKEND_CORS_ORIGINS", mode="before")
    @classmethod
    def assemble_cors_origins(cls, value: str | list[str]) -> list[str] | str:
        if isinstance(value, str) and not value.startswith("["):
            return [i.strip() for i in value.split(",")]
        elif isinstance(value, (list, str)):
            return value
        raise ValueError(value)

    {% if cookiecutter.database == "Beanie" -%}
    DATABASE_URI: AnyUrl
    {% endif -%}
    {% if cookiecutter.database == "Tortoise" -%}
    DATABASE_URI: PostgresDsn
    {% endif %}

    {% if cookiecutter.mail_service == 'Other SMTP' -%}
    SMTP_TLS: bool = True
    SMTP_PORT: int | None = None
    SMTP_HOST: str | None = None
    SMTP_USERNAME: str | None = None
    SMTP_PASSWORD: str | None = None
    {% elif cookiecutter.mail_service == 'Amazon SES' -%}
    SES_ACCESS_KEY: str | None = None
    SES_SECRET_KEY: str | None = None
    SES_REGION: str | None = None
    {% endif -%}
    DEFAULT_FROM_EMAIL: EmailStr
    DEFAULT_FROM_NAME: str | None = None
    EMAILS_ENABLED: bool = False

    @field_validator("EMAILS_ENABLED", mode="before")
    @classmethod
    def get_emails_enabled(cls, value: bool, info: ValidationInfo) -> bool:
        return bool(
            info.data.get("SMTP_HOST")
            and info.data.get("SMTP_PORT")
            and info.data.get("DEFAULT_FROM_EMAIL")
        )

    FIRST_SUPERUSER_EMAIL: EmailStr
    FIRST_SUPERUSER_PASSWORD: str


settings = Settings()
