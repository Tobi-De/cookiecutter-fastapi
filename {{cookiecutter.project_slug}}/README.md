# {{cookiecutter.project_name}}

{{cookiecutter.project_description}}


## Prerequisites

- `Python 3.9+`
- `uv`
- `Postgresql 10+`


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

```shell
python manage.py work
```

### Cli

There is a manage.py file at the root of the project, it contains a basic cli to hopefully
help you manage your project more easily. To get all available commands type this:

```shell
python manage.py --help
```

## Credits

This package was created with [Cookiecutter](https://github.com/cookiecutter/cookiecutter) and the [cookiecutter-fastapi](https://github.com/tobi-de/cookiecutter-fastapi) project template.
