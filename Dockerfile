FROM python:3.12

ENV POETRY_VERSION=1.8.3

WORKDIR /app
ENV PYTHONPATH=/app
COPY src .
COPY pyproject.toml .

RUN apt-get update && apt-get install -y iproute2
RUN pip install poetry==${POETRY_VERSION}
RUN poetry install --no-root
