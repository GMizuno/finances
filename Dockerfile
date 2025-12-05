# Use uma imagem base leve
FROM python:3.11-slim

# Variáveis de ambiente para evitar arquivos .pyc e logs em buffer
ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    POETRY_VERSION=1.8.2

# Instalar dependências do sistema necessárias (opcional, dependendo dos seus pacotes)
RUN apt-get update && apt-get install -y --no-install-recommends \
    gcc \
    libpq-dev \
    && rm -rf /var/lib/apt/lists/*

# Instalar o Poetry via pip
RUN pip install "poetry==$POETRY_VERSION"

# Definir diretório de trabalho
WORKDIR /app

# Copiar apenas os arquivos de dependência primeiro (para cache do Docker)
COPY pyproject.toml poetry.lock ./

# Configurar o Poetry para NÃO criar virtualenv (instala direto no sistema do container)
RUN poetry config virtualenvs.create false

# Instalar dependências de produção (sem dev dependencies)
RUN poetry install --no-root --only main

# Copiar o restante do código da aplicação
COPY . .

# Comando de inicialização (ajuste conforme seu script ou framework, ex: FastAPI, Flask)
CMD ["python", "main.py"]
