FROM python:3.12.5-slim-bullseye

ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1
# TODO: remove
ENV PYTHONPATH=/

WORKDIR /src

RUN apt update -y && \
    apt install -y python3-dev \
    gcc \
    musl-dev

ADD pyproject.toml /src

RUN pip install --upgrade pip
RUN pip install poetry

RUN poetry install --no-root --no-interaction

COPY /src/ /src/
COPY /tests/ /tests/
COPY /docker_compose/entrypoint.sh /src/entrypoint.sh