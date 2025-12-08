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

# --- CORREÇÃO 1: Remova a linha que desativa o virtualenv ---
# A variável de ambiente POETRY_VIRTUALENVS_IN_PROJECT=1 já garante que ele será criado em /app/.venv
RUN poetry install --no-root --only main && rm -rf $POETRY_CACHE_DIR

# --- CORREÇÃO 2: Instale o awslambdaric se ele não estiver no pyproject.toml ---
# Se ele já estiver no seu pyproject.toml, pode remover esta linha abaixo.
# Caso contrário, o ENTRYPOINT vai falhar.
RUN ./.venv/bin/pip install awslambdaric

FROM python:3.12-slim as runtime

# Define o local onde a AWS Lambda espera o código (opcional, mas recomendado)
ARG LAMBDA_TASK_ROOT="/var/task"

ENV VIRTUAL_ENV=${LAMBDA_TASK_ROOT}/.venv \
    PATH="${LAMBDA_TASK_ROOT}/.venv/bin:$PATH" \
    LAMBDA_TASK_ROOT=${LAMBDA_TASK_ROOT}

WORKDIR ${LAMBDA_TASK_ROOT}

# --- CORREÇÃO 3: Copia o venv e o código para o local correto ---
# Copia o venv criado no builder
COPY --from=builder /app/.venv ${LAMBDA_TASK_ROOT}/.venv

# Copia o código fonte
COPY . ${LAMBDA_TASK_ROOT}

# O Entrypoint usa o python do PATH (que agora aponta para o .venv)
ENTRYPOINT [ "python", "-m", "awslambdaric" ]

# Seu comando original
CMD ["main.main"]