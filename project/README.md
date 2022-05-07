# {{cookiecutter.project_name}}

{{cookiecutter.project_description}}

## Database setup

Aerich initialization, should be done only once.

```shell
aerich init -t app.db.init_db.TORTOISE_ORM
```

Create migrations

```shell
aerich init-db
```

Adding new migrations.

```shell
aerich migrate --name <migration_name>
```

Upgrading the database when new database are created.

```shell
aerich upgrade
```


## Run the fastapi app

```shell
uvicorn app.main:app
```

## Run arq

```shell
 arq app.worker.WorkerSettings
```
