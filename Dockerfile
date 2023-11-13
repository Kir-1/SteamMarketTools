FROM python:3.11-alpine


ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1


WORKDIR /code

RUN pip install --upgrade pip
RUN pip install poetry

COPY pyproject.toml .
COPY poetry.lock .
COPY alembic ./alembic
COPY alembic.ini .
COPY .env .
RUN poetry config virtualenvs.create false
RUN poetry install --no-root --no-interaction --no-ansi

COPY src ./src



