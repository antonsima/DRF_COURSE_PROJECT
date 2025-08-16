FROM python:3.12-slim

WORKDIR /app

RUN apt-get update \
    && apt-get install -y gcc libpq-dev \
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/*

COPY pyproject.toml poetry.lock* ./

RUN pip install celery && pip install poetry && poetry install --no-root

COPY . .

RUN mkdir -p /app/media

EXPOSE 8000

CMD ['python', 'manage.py', 'runserver', '0.0.0.0:8000']