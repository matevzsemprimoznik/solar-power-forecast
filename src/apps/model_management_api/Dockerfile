FROM python:3.12-slim as builder

RUN pip install poetry==1.4.2

ENV POETRY_NO_INTERACTION=1 \
    POETRY_VIRTUALENVS_IN_PROJECT=1 \
    POETRY_VIRTUALENVS_CREATE=1 \
    POETRY_CACHE_DIR=/tmp/poetry_cache

WORKDIR /app

COPY pyproject.toml poetry.lock ./
RUN touch README.md

RUN --mount=type=cache,target=$POETRY_CACHE_DIR poetry install --without dev --without dev-win --no-root

FROM python:3.12-slim as runtime

ENV VIRTUAL_ENV=/app/.venv \
    PATH="/app/.venv/bin:$PATH"

COPY --from=builder ${VIRTUAL_ENV} ${VIRTUAL_ENV}

COPY src/apps/model_management_api ./app/src/apps/model_management_api

COPY src/config ./app/src/config

COPY src/models ./app/src/models

WORKDIR /app

CMD ["uvicorn", "src.apps.model_management_api.main:app", "--host", "0.0.0.0", "--port", "5000"]