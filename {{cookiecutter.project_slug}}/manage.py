from __future__ import annotations

import asyncio
from functools import partial
from itertools import chain

import typer
import uvicorn
from aiosmtpd.controller import Controller
from aiosmtpd.handlers import Debugging
from fastapi_users.exceptions import InvalidPasswordException, UserAlreadyExists
from tortoise import Tortoise, connections
from traitlets.config import Config

from app.core.config import settings
from app.db.config import TORTOISE_ORM
from app.users import utils
from app.users.schemas import UserCreate

cli = typer.Typer()


@cli.command(help="Run the uvicorn server.")
def runserver(
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


@cli.command(help="Create a new user.")
def create_user():
    """Create a new user"""
    email = typer.prompt("email", type=str)
    password = typer.prompt("password", type=str, hide_input=True)
    full_name = typer.prompt("full name", type=str, default="")
    short_name = typer.prompt("short name", type=str, default="")
    superuser = typer.prompt("is superuser?", type=bool, default=False)

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


@cli.command(help="An Ipython shell with your database models automatically imported.")
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


@cli.command(help="Run the arq worker.")
def worker():
    """Run the worker process"""
    import subprocess

    subprocess.run(
        [
            "arq",
            "app.worker.WorkerSettings",
            "--watch",
            settings.BASE_DIR.resolve(strict=True),
        ]
    )


@cli.command(help="Create a new app component.")
def startapp(app_name: str):
    """Create a new fastapi component similarly to django startapp"""
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


@cli.command(help="Starts a test mail server for development.")
def mailserver(hostname: str = "localhost", port: int = 8025):
    """Run a simple smtp server, if you use tools like mailhog, you can delete this"""
    typer.secho(f"Now accepting mail at {hostname}:{port}", fg=typer.colors.GREEN)
    controller = Controller(Debugging(), hostname=hostname, port=port)
    controller.start()
    while True:
        pass


if __name__ == "__main__":
    cli()
