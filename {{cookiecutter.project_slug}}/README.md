# {{cookiecutter.project_name}}

{{cookiecutter.project_description}}

## Database setup

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

## Run the fastapi app

```shell
python manage.py runserver
```

## Cli

There is a manage.py file at the root of the project, it contains a basic cli to hopefully
help you manage your project more easily. To get all available commands type this:

```shell
python manage.py --help
```

