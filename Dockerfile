FROM python:3.11

WORKDIR /app

ENV PYTHONDONTWRITEBYTECODE  1
ENV PYTHONUNBUFFERED 1

COPY pyproject.toml ./
RUN pip3 install poetry
RUN  poetry config virtualenvs.create false &&  poetry install --no-interaction --no-ansi --no-root

COPY . .