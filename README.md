# Fastapi Cookiecutter

A [Cookiecutter]() for fastapi projects, inspired by [cookiecutter-django](https://github.com/cookiecutter/cookiecutter-django).

[![MIT License](https://img.shields.io/apm/l/atomic-design-ui.svg?)](https://github.com/Tobi-De/cookiecutter-fastapi/blob/master/LICENSE)
[![black](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/psf/black)


## Features

- [x] Use [fastapi-users](https://github.com/fastapi-users/fastapi-users) for users authentication and management
- [x] [Pydantic](https://pydantic-docs.helpmanual.io/) for settings management
- [x] Include a cli tool built with [typer](https://github.com/tiangolo/typer) to simplify project management
- [x] [Pre-commit](https://pre-commit.com/) integration included by default
- [x] [Tortoise-orm](https://tortoise.github.io/) and [aerich](https://github.com/tortoise/aerich) database setup by default but switchable
- [x] [Fastapi-pagination](https://github.com/uriyyo/fastapi-pagination) included by default
- [x] Run tests with unittest or [pytest](https://docs.pytest.org/en/7.1.x/)
- [x] Sending emails using [aiosmtplib](https://aiosmtplib.readthedocs.io/en/stable/client.html)
- [x] Optional integration with [sentry](https://docs.sentry.io/platforms/python/) for error logging
- [ ] [Docker](https://www.docker.com/) and [docker-compose](https://github.com/docker/compose) for and production using [Traefik](https://github.com/traefik/traefik)
- [ ] Optional setup of HTML templates rendering using [jinja2](https://jinja.palletsprojects.com/en/3.1.x/)
- [ ] Optional static files serving using [whitenoise](http://whitenoise.evans.io/en/stable/)
- [ ] [Procfile](https://devcenter.heroku.com/articles/procfile) for deploying to heroku
- [ ] Optional integration with [fastapi-storages](https://github.com/Tobi-De/fastapi-storages) for media files storage
- [ ] Implement the Health [Check API pattern](https://microservices.io/patterns/observability/health-check-api.html) on your FastAPI application
- [ ] Renders fastapi projects with 100% starting test coverage

### Task queues manager options

 - [x] [Arq](https://github.com/samuelcolvin/arq)
 - [ ] [Procrastinate](https://github.com/procrastinate-org/procrastinate)
 - [ ] [Celery](https://github.com/celery/celery)

### Database options

- [x] [Tortoise ORM](https://tortoise.github.io/)
- [ ] [RedisOM](https://github.com/redis/redis-om-python)
- [ ] [Beanie](https://github.com/roman-right/beanie)
- [ ] [SQLModel](https://github.com/tiangolo/sqlmodel)


## Usage

Install the cookiecutter package:

```shell
pip install cookiecutter
```

Now run it against this repo:

```shell
cookiecutter https://github.com/Tobi-De/cookiecutter-fastapi
```

You'll be prompted for some values. Provide them, then a fastapi project will be created for you.
