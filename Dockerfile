FROM python:3.12 as builder

ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    POETRY_VERSION=1.8.2 \
    POETRY_NO_INTERACTION=1 \
    POETRY_VIRTUALENVS_IN_PROJECT=1 \
    POETRY_VIRTUALENVS_CREATE=1 \
    POETRY_CACHE_DIR=/tmp/poetry_cache

RUN apt-get update && apt-get install -y --no-install-recommends \
    gcc \
    libpq-dev \
    && rm -rf /var/lib/apt/lists/*

RUN pip install "poetry==$POETRY_VERSION"

WORKDIR /app

COPY pyproject.toml poetry.lock ./

RUN poetry install --no-root --only main && rm -rf $POETRY_CACHE_DIR

RUN ./.venv/bin/pip install awslambdaric

FROM python:3.12-slim as runtime

ARG LAMBDA_TASK_ROOT="/var/task"

ENV VIRTUAL_ENV=${LAMBDA_TASK_ROOT}/.venv \
    PATH="${LAMBDA_TASK_ROOT}/.venv/bin:$PATH" \
    LAMBDA_TASK_ROOT=${LAMBDA_TASK_ROOT}

WORKDIR ${LAMBDA_TASK_ROOT}

COPY --from=builder /app/.venv ${LAMBDA_TASK_ROOT}/.venv

COPY . ${LAMBDA_TASK_ROOT}

ENTRYPOINT [ "python", "-m", "awslambdaric" ]

CMD ["main.main"]