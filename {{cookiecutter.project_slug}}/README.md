# {{cookiecutter.project_name}}

{{cookiecutter.project_description}}


## Prerequisites

- `Python 3.9+`
- `uv`
- `Postgresql 10+`
- `just` (optional, for using the justfile commands)


## Quick Start

This project includes a justfile with common commands following the [scripts-to-rule-them-all](https://github.com/github/scripts-to-rule-them-all) pattern.

To see all available commands:

```shell
just --list
```

### First-time setup

```shell
# Install dependencies and set up the project
just setup
```

### Running the development server

```shell
# Start the development server
just server

# Or run all services (server, worker, redis) together
just work
```

### Other common commands

```shell
# Run tests
just test

# Open an interactive console
just console

# Create a new user
just create-user

# See project information
just info
```


## Development

### `.env` example

```shell
DEBUG=True
SERVER_HOST=http://localhost:8000
SECRET_KEY=qwtqwubYA0pN1GMmKsFKHMw_WCbboJvdTAgM9Fq-UyM
SMTP_PORT=1025
SMTP_HOST=localhost
SMTP_TLS=False
BACKEND_CORS_ORIGINS=["http://localhost"]
DATABASE_URI=postgres://postgres:password@localhost/{{cookiecutter.project_slug}}
DEFAULT_FROM_EMAIL={{cookiecutter.project_name}}@gmail.com
REDIS_URL=redis://localhost
FIRST_SUPERUSER_EMAIL=admin@mail.com
FIRST_SUPERUSER_PASSWORD=admin
```

### Database setup

Create your first migration

```shell
aerich init-db
```

Adding new migrations.

```shell
aerich migrate --name <migration_name>
```

Upgrading the database when new migrations are created.

```shell
aerich upgrade
```

### Run the fastapi app

Using the new FastAPI CLI (recommended):

```shell
# Run in development mode with auto-reload
python -m app dev

# Or using the shorthand
fastapi dev

# Run all services (server, worker, redis) together
python -m app work
```

Using the traditional method (still supported):

```shell
python manage.py work
```

### CLI Commands

The project includes a comprehensive CLI built with Typer, now integrated with the official FastAPI CLI. 
The CLI is available through both the new `python -m app` interface and the legacy `python manage.py` interface.

**Available via FastAPI CLI integration:**
- `dev` - Run the development server with auto-reload (powered by FastAPI CLI)
- `run` - Run the production server (powered by FastAPI CLI)

**Custom project commands:**
- `work` - Run all development services (server, worker, redis) in one command
- `run-server` - Run the development server (uvicorn)
- `run-prod-server` - Run the production server (gunicorn)
- `create-user` - Interactively create a new user
- `start-app` - Create a new FastAPI component (similar to Django's startapp)
{% if cookiecutter.database == "Tortoise" -%}
- `migrate-db` - Apply database migrations
- `shell` - Open an interactive IPython shell with auto-imports
{% endif -%}
- `run-worker` - Run the SAQ worker process
- `run-mailserver` - Run a test SMTP server for development
- `secret-key` - Generate a secure secret key
- `info` - Show project health and settings

To see all available commands:

```shell
# New way (recommended)
python -m app --help

# Legacy way (still works)
python manage.py --help
```

Example usage:

```shell
# Start development server with FastAPI CLI
python -m app dev

# Create a new user
python -m app create-user

# Generate a secret key
python -m app secret-key

# Run all services together
python -m app work
```

## Credits

This package was created with [Cookiecutter](https://github.com/cookiecutter/cookiecutter) and the [cookiecutter-fastapi](https://github.com/tobi-de/cookiecutter-fastapi) project template.
