# Django, Celery, & Flower

FROM python:3.12-slim

RUN apt-get update && apt-get install -y \
    build-essential \
    libpq-dev \
    && rm -rf /var/lib/apt/lists/*

WORKDIR /app

COPY pyproject.toml poetry.lock ./


RUN pip install poetry
RUN poetry export --without-hashes -f requirements.txt -o /tmp/requirements.txt
RUN pip install --no-cache-dir -r /tmp/requirements.txt

RUN pip install watchdog

COPY . .
