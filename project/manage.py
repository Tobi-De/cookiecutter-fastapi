from __future__ import annotations

from asyncio import run as aiorun

import typer
import uvicorn
from fastapi_users.manager import InvalidPasswordException, UserAlreadyExists
from pydantic import EmailStr
from tortoise import Tortoise
from traitlets.config import Config

from app.core.config import settings
from app.db.config import TORTOISE_ORM
from app.users import models as user_models, schemas as user_schemas
from app.users.utils import create_user

cli = typer.Typer()


# todo reset_db ?
#   startapp


@cli.command()
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


@cli.command()
def create_user():
    """Create user"""
    email = typer.prompt("email", type=EmailStr)
    password = typer.prompt("password", type=str, hide_input=True)
    full_name = typer.prompt("full name", type=str, default="")
    short_name = typer.prompt("short name", type=str, default="")
    superuser = typer.prompt("is superuser?", type=bool, default=False)

    async def _create_user():
        await Tortoise.init(config=TORTOISE_ORM)
        await create_user(
            user_schemas.UserCreate(
                email=email,
                password=password,
                full_name=full_name,
                short_name=short_name,
                superuser=superuser,
            )
        )

    try:
        aiorun(_create_user())
    except UserAlreadyExists:
        typer.echo(f"user with {email} already exists")
    except InvalidPasswordException:
        typer.echo(f"Invalid password")
    else:
        typer.echo(f"user {email} created")


@cli.command()
def shell():
    """Opens an interactive shell with objects auto imported"""

    _vars = {
        "db": db,
        "settings": settings,
        "cli": cli,
        "user_models": user_models,
        "user_schemas": user_schemas,
    }
    typer.echo(f"Auto imports: {list(_vars.keys())}")
    try:
        from IPython import start_ipython

        c = Config()
        c.InteractiveShell.autoawait = True
        c.InteractiveShellApp.exec_lines = [
            "from tortoise import Tortoise",
            "from app.db.config import TORTOISE_ORM",
            "await Tortoise.init(config=TORTOISE_ORM)",
        ]
        start_ipython(argv=[], user_ns=_vars, config=c)
    except ImportError:
        typer.echo("Install iPython using `poetry add ipython` to use this feature.")


@cli.command()
def worker():
    import subprocess
    subprocess.run(["arq", "app.worker.WorkerSettings", "--watch", settings.BASE_DIR.resolve(strict=True)])


if __name__ == "__main__":
    cli()
