# Cookiecutter Fastapi

[![PyPI](https://img.shields.io/pypi/v/cookiecutter-fastapi.svg)][pypi_]
[![Status](https://img.shields.io/pypi/status/cookiecutter-fastapi.svg)][status]
[![Read the documentation at https://cookiecutter-fastapi.readthedocs.io/](https://img.shields.io/readthedocs/cookiecutter-fastapi/latest.svg?label=Read%20the%20Docs)][read the docs]
[![python](https://img.shields.io/pypi/pyversions/cookiecutter-fastapi)](https://github.com/Tobi-De/cookiecutter-fastapi)
[![MIT License](https://img.shields.io/apm/l/atomic-design-ui.svg?)](https://github.com/Tobi-De/cookiecutter-fastapi/blob/master/LICENSE)
[![black](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/psf/black)

[read the docs]: https://cookiecutter-fastapi.readthedocs.io/
[pypi_]: https://pypi.org/project/fastapi-paginator/
[status]: https://pypi.org/project/fastapi-paginator/

A [Cookiecutter](https://github.com/audreyr/cookiecutter) template for [fastapi](https://fastapi.tiangolo.com) projects, inspired by [cookiecutter-django](https://github.com/cookiecutter/cookiecutter-django).

✨📚✨ [Read the full documentation][read the docs]

## Features

<!-- features-begin -->

- [x] [fastapi-users](https://github.com/fastapi-users/fastapi-users) for users authentication and management
- [x] [Pydantic](https://pydantic-docs.helpmanual.io/) for settings management
- [x] Include a cli tool built with [typer](https://github.com/tiangolo/typer) to simplify project management
- [x] [Pre-commit](https://pre-commit.com/) integration included by default
- [x] [Tortoise-orm](https://tortoise.github.io/) and [aerich](https://github.com/tortoise/aerich) database setup by default but switchable
- [x] Limit-offset pagination helpers included
- [x] Run tests with unittest or [pytest](https://docs.pytest.org/en/7.1.x/)
- [x] Sending emails using [aiosmtplib](https://aiosmtplib.readthedocs.io/en/stable/client.html) or [Amazon SES](https://aws.amazon.com/fr/ses/)
- [x] Optional integration with [sentry](https://docs.sentry.io/platforms/python/) for error logging
- [ ] [Docker](https://www.docker.com/) and [docker-compose](https://github.com/docker/compose) for production using [Traefik](https://github.com/traefik/traefik)
- [x] Optional setup of HTML templates rendering using [jinja2](https://jinja.palletsprojects.com/en/3.1.x/)
- [ ] Optional static files serving using [whitenoise](http://whitenoise.evans.io/en/stable/)
- [x] [Procfile](https://devcenter.heroku.com/articles/procfile) for deploying to heroku
- [ ] Optional integration with [fastapi-storages](https://github.com/Tobi-De/fastapi-storages) for media files storage
- [x] Implement the [Health Check API patterns](https://microservices.io/patterns/observability/health-check-api.html) on your fastapi application
- [ ] Renders fastapi projects with 100% starting test coverage

### Task queues manager options

 - [x] [Arq](https://github.com/samuelcolvin/arq)
 - [ ] [Procrastinate](https://github.com/procrastinate-org/procrastinate)
 - [ ] [Celery](https://github.com/celery/celery)

### ORM/ODM options

- [x] [Tortoise ORM](https://tortoise.github.io/)
- [ ] [RedisOM](https://github.com/redis/redis-om-python)
- [ ] [Beanie](https://github.com/roman-right/beanie)
- [ ] [SQLModel](https://github.com/tiangolo/sqlmodel)

<!-- features-end -->

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

## Contributing

Contributions are very welcome. To learn more, see the [Contributor Guide].

## License

Distributed under the terms of the [MIT license][license],
_Cookiecutter Fastapi_ is free and open source software.

## Issues

If you encounter any problems,
please [file an issue] along with a detailed description.

[file an issue]: https://github.com/tobi-de/cookiecutter-fastapi/issues

<!-- github-only -->

[license]: https://github.com/tobi-de/cookiecutter-fastapi/blob/main/LICENSE
[contributor guide]: https://github.com/tobi-de/cookiecutter-fastapi/blob/main/CONTRIBUTING.md
