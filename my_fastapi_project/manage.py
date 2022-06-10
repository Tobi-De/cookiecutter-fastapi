from __future__ import annotations

import asyncio
import logging
import secrets
from functools import partial
from itertools import chain
from typing import cast

import httpx
import typer
import uvicorn
from aiosmtpd.controller import Controller
from aiosmtpd.handlers import Debugging
from arq.cli import watch_reload, run_worker as run_arq_worker
from arq.logs import default_log_config
from arq.typing import WorkerSettingsType
from email_validator import EmailNotValidError, validate_email
from fastapi_users.exceptions import InvalidPasswordException, UserAlreadyExists
from tortoise import Tortoise, connections
from traitlets.config import Config

from app.core.config import settings
from app.db.config import TORTOISE_ORM
from app.users import utils
from app.users.schemas import UserCreate
from app.worker import WorkerSettings

cli = typer.Typer()


def _validate_email(val: str):
    try:
        validate_email(val)
    except EmailNotValidError:
        raise typer.BadParameter(f"{val} is not a valid email")
    return val


@cli.command("run-server")
def run_server(
    port: int = 8000,
    host: str = "localhost",
    log_level: str = "debug",
    reload: bool = True,
):
    """Run the API server."""
    uvicorn.run(
        "app.main:app",
        host=host,
        port=port,
        log_level=log_level,
        reload=reload,
    )


@cli.command("create-user")
def create_user(
    email: str = typer.Option(..., prompt=True, callback=_validate_email),
    password: str = typer.Option(..., prompt=True, hide_input=True),
    full_name: str = typer.Option("", prompt=True),
    short_name: str = typer.Option("", prompt=True),
    superuser: bool = typer.Option(False, prompt=True),
):
    """Create a new user."""

    async def _create_user():
        await Tortoise.init(config=TORTOISE_ORM)
        await utils.create_user(
            UserCreate(
                email=email,
                password=password,
                full_name=full_name,
                short_name=short_name,
                superuser=superuser,
            )
        )
        await connections.close_all()

    try:
        asyncio.run(_create_user())
    except UserAlreadyExists:
        typer.secho(f"user with {email} already exists", fg=typer.colors.BLUE)
    except InvalidPasswordException:
        typer.secho("Invalid password", fg=typer.colors.RED)
    else:
        typer.secho(f"user {email} created", fg=typer.colors.GREEN)


@cli.command("start-app")
def start_app(app_name: str):
    """Create a new fastapi component, similar to django startapp"""
    package_name = app_name.lower().strip().replace(" ", "_").replace("-", "_")
    app_dir = settings.BASE_DIR / package_name
    files = {
        "__init__.py": "",
        "models.py": "from app.db.models import TimeStampedModel",
        "schemas.py": "from pydantic import BaseModel",
        "routes.py": f"from fastapi import APIRouter\n\nrouter = APIRouter(prefix='/{package_name}')",
        "tests/__init__.py": "",
        "tests/factories.py": "from factory import Factory, Faker",
    }
    app_dir.mkdir()
    (app_dir / "tests").mkdir()
    for file, content in files.items():
        with open(app_dir / file, "w") as f:
            f.write(content)
    typer.secho(f"App {package_name} created", fg=typer.colors.GREEN)


@cli.command()
def shell():
    """Opens an interactive shell with objects auto imported"""
    try:
        from IPython import start_ipython
    except ImportError:
        typer.secho(
            "Install iPython using `poetry add ipython` to use this feature.",
            fg=typer.colors.RED,
        )
        raise typer.Exit()

    def teardown_shell():
        import asyncio

        print("closing tortoise connections....")
        asyncio.run(connections.close_all())

    tortoise_init = partial(Tortoise.init, config=TORTOISE_ORM)
    modules = list(
        chain(*[app.get("models") for app in TORTOISE_ORM.get("apps").values()])
    )
    auto_imports = [
        "from tortoise.expressions import Q, F, Subquery",
        "from tortoise.query_utils import Prefetch",
    ] + [f"from {module} import *" for module in modules]
    shell_setup = [
        "import atexit",
        "_ = atexit.register(teardown_shell)",
        "await tortoise_init()",
    ]
    typer.secho("Auto Imports\n" + "\n".join(auto_imports), fg=typer.colors.GREEN)
    c = Config()
    c.InteractiveShell.autoawait = True
    c.InteractiveShellApp.exec_lines = auto_imports + shell_setup
    start_ipython(
        argv=[],
        user_ns={"teardown_shell": teardown_shell, "tortoise_init": tortoise_init},
        config=c,
    )


@cli.command("run-worker")
def run_worker(watch: bool = typer.Option(False)):
    """Run the arq worker process"""
    logging.config.dictConfig(default_log_config(True))
    conf = cast(WorkerSettingsType, WorkerSettings)
    if watch:
        asyncio.new_event_loop().run_until_complete(
            watch_reload(
                settings.BASE_DIR.resolve(strict=True),
                conf,
            )
        )
    else:
        run_arq_worker(conf)


@cli.command(help="run-mailserver")
def run_mailserver(hostname: str = "localhost", port: int = 1025):
    """Run a test smtp server, for development purposes only, for a more robust option try MailHog"""
    typer.secho(f"Now accepting mail at {hostname}:{port}", fg=typer.colors.GREEN)
    controller = Controller(Debugging(), hostname=hostname, port=port)
    controller.start()
    while True:
        pass


@cli.command("secret-key")
def secret_key():
    """Generate a secret key for your application"""
    typer.secho(f"{secrets.token_urlsafe(64)}", fg=typer.colors.GREEN)


@cli.command()
def info():
    """Show project health and settings."""
    with httpx.Client(base_url=settings.SERVER_HOST) as client:
        try:
            resp = client.get("/health", follow_redirects=True)
        except httpx.ConnectError:
            app_health = typer.style(
                "❌ API is not responding", fg=typer.colors.RED, bold=True
            )
        else:
            app_health = "\n".join(
                [f"{key.upper()}={value}" for key, value in resp.json().items()]
            )

    envs = "\n".join(
        [f"{key}={value}" for key, value in settings.dict().items()]
    )
    title = typer.style("===> APP INFO <==============\n", fg=typer.colors.BLUE)
    typer.secho(title + app_health + "\n" + envs)


if __name__ == "__main__":
    cli()
