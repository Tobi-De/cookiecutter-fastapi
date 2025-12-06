from __future__ import annotations

import os
import sys
import asyncio
import secrets
import subprocess
from functools import partial
from itertools import chain
from pathlib import Path

import httpx
import typer
import uvicorn
from email_validator import EmailNotValidError, validate_email
from fastapi_users.exceptions import InvalidPasswordException, UserAlreadyExists
{% if cookiecutter.database == "Tortoise" -%}
from tortoise import Tortoise, connections
{% endif -%}
from honcho.manager import Manager as HonchoManager

from {{cookiecutter.project_slug}}.core.config import settings
{% if cookiecutter.database == "Tortoise" -%}
from {{cookiecutter.project_slug}}.db.config import TORTOISE_ORM
{% endif -%}
from {{cookiecutter.project_slug}}.users import utils
from {{cookiecutter.project_slug}}.users.schemas import UserCreate

# Main CLI app
cli = typer.Typer()


def _validate_email(val: str):
    try:
        validate_email(val)
    except EmailNotValidError:
        raise typer.BadParameter(f"{val} is not a valid email")
    return val


# Integrate FastAPI CLI commands
from fastapi_cli.cli import app as fastapi_cli_app

# Add FastAPI CLI commands (dev and run) to our CLI
# Note: We directly append to registered_commands as this is the standard
# way to programmatically add commands to a Typer app in this context
for cmd_info in fastapi_cli_app.registered_commands:
    cli.registered_commands.append(cmd_info)


# Custom commands from the original manage.py
{% if cookiecutter.database == "Tortoise" -%}
@cli.command("migrate-db")
def migrate_db():
    """Apply database migrations"""
    subprocess.run(("aerich", "upgrade"))
{% endif %}


@cli.command("work")
def work(mailserver: bool = typer.Option(False)):
    """Run all the dev services in a single command."""
    manager = HonchoManager()
    project_env = {
        **os.environ,
        "PYTHONPATH": str(Path().resolve(strict=True)),
        "PYTHONUNBUFFERED": "true",
    }
    manager.add_process("redis", "redis-server")
    {% if cookiecutter.database == "Tortoise" -%}
    manager.add_process("server", f"aerich upgrade && {sys.executable} -m {{cookiecutter.project_slug}} dev", env=project_env)
    {% else %}
    manager.add_process("server", f"{sys.executable} -m {{cookiecutter.project_slug}} dev", env=project_env)
    {% endif -%}
    manager.add_process("worker", f"{sys.executable} -m {{cookiecutter.project_slug}} run-worker", env=project_env)
    if mailserver:
        manager.add_process("mailserver", f"{sys.executable} -m {{cookiecutter.project_slug}} run-mailserver")

    manager.loop()
    sys.exit(manager.returncode)


@cli.command("run-server")
def run_server(
    port: int = 8000,
    host: str = "localhost",
    log_level: str = "debug",
    reload: bool = True,
):
    """Run the API development server(uvicorn)."""
    {% if cookiecutter.database == "Tortoise" -%}
    migrate_db()
    {% endif -%}
    uvicorn.run(
        "{{cookiecutter.project_slug}}.main:app",
        host=host,
        port=port,
        log_level=log_level,
        reload=reload,
    )


@cli.command("run-prod-server")
def run_prod_server():
    """Run the API production server(gunicorn)."""
    from gunicorn.app.base import Application
    from gunicorn import util

    config_file = str(
        settings.PATHS.ROOT_DIR.joinpath("gunicorn.conf.py").resolve(strict=True)
    )

    class APPServer(Application):
        def init(self, parser, opts, args):
            pass

        def load_config(self):
            self.load_config_from_file(config_file)

        def load(self):
            return util.import_app("{{cookiecutter.project_slug}}.main:app")

    {% if cookiecutter.database == "Tortoise" -%}
    migrate_db()
    {% endif -%}
    APPServer().run()


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
        {% if cookiecutter.database == "Tortoise" -%}
        await Tortoise.init(config=TORTOISE_ORM)
        {% endif -%}
        await utils.create_user(
            UserCreate(
                email=email,
                password=password,
                full_name=full_name,
                short_name=short_name,
                superuser=superuser,
            )
        )
        {%- if cookiecutter.database == "Tortoise" %}
        await connections.close_all()
        {%- endif %}

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
        "models.py": "from {{cookiecutter.project_slug}}.db.models import TimeStampedModel",
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


{% if cookiecutter.database == "Tortoise" -%}
@cli.command()
def shell():
    """Opens an interactive shell with objects auto imported"""
    try:
        from IPython import start_ipython
        from traitlets.config import Config
    except ImportError:
        typer.secho(
            "Install iPython using `uv add --dev ipython` to use this feature.",
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
{% endif -%}


@cli.command("run-worker")
def run_worker(reload: bool = typer.Option(True)):
    """Run the saq worker process"""
    if reload:
        subprocess.run(["hupper", "-m", "saq", "{{cookiecutter.project_slug}}.worker.settings", "--web"])
    else:
        subprocess.run(["python", "-m", "saq", "{{cookiecutter.project_slug}}.worker.settings", "--web"])


@cli.command(help="run-mailserver")
def run_mailserver(hostname: str = "localhost", port: int = 1025):
    """Run a test smtp server, for development purposes only, for a more robust option try MailHog"""
    from aiosmtpd.controller import Controller
    from aiosmtpd.handlers import Debugging

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
    with httpx.Client(base_url=str(settings.SERVER_HOST)) as client:
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

    envs = "\n".join([f"{key}={value}" for key, value in settings.model_dump().items()])
    title = typer.style("===> APP INFO <==============\n", fg=typer.colors.BLUE)
    typer.secho(title + app_health + "\n" + envs)


if __name__ == "__main__":
    cli()
