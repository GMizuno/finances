FROM public.ecr.aws/lambda/python:3.12

# 1. Instalar o Poetry
# Usamos pip para instalar o poetry dentro da imagem base
RUN pip install poetry

# 2. Copiar os arquivos de definição de dependências do Poetry
# Copiamos para o diretório de tarefa do Lambda (${LAMBDA_TASK_ROOT})
COPY pyproject.toml poetry.lock ${LAMBDA_TASK_ROOT}/

# 3. Instalar as dependências do projeto
# --config virtualenvs.create false: Instala as libs diretamente no ambiente do Python (não cria venv)
# --only main: Instala apenas dependências de produção (ignora as de desenvolvimento)
# --no-root: Não instala o próprio pacote do projeto (pois copiaremos o código fonte depois)
RUN poetry config virtualenvs.create false && \
    poetry install --no-interaction --no-ansi --only main --no-root

# 4. Copiar o código da função
COPY app.py ${LAMBDA_TASK_ROOT}

# 5. Definir o CMD para o manipulador da função (handler)
CMD [ "app.handler" ]