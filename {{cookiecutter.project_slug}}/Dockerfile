FROM python:3.10 as requirements-stage

WORKDIR /tmp

RUN pip install poetry

COPY ./pyproject.toml ./poetry.lock* /tmp/

RUN poetry export -f requirements.txt --output requirements.txt --without-hashes

FROM python:3.10-alpine

WORKDIR /code

RUN apk update \
    && apk add --virtual build-deps build-base \
    && apk add --no-cache libffi-dev redis \
    && pip install --upgrade pip supervisor \
    && python --version

COPY --from=requirements-stage /tmp/requirements.txt /code/requirements.txt

RUN pip install --no-cache-dir --upgrade -r /code/requirements.txt

COPY supervisord.conf /etc/supervisord.conf

COPY ./ /code

ENV PORT=8000
EXPOSE ${PORT}

CMD ["supervisord", "-c", "/etc/supervisord.conf"]

