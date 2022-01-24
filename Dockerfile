# All in one (monolith) Dockerfile, FastAPI serves static assets
# NOTE: Keep steps in this Dockerfile synced with the individual frontend and backend Dockerfiles

FROM node:15 as frontend-build-stage

WORKDIR /app

COPY frontend/package.json frontend/yarn.lock /app/

RUN yarn install --frozen-lockfile

COPY ./frontend /app/

ARG FRONTEND_ENV=production

ENV VUE_APP_ENV=${FRONTEND_ENV}

RUN NODE_ENV=production yarn build


FROM tiangolo/uvicorn-gunicorn-fastapi:python3.8

WORKDIR /app/

RUN curl -sSL https://raw.githubusercontent.com/python-poetry/poetry/master/get-poetry.py | POETRY_HOME=/opt/poetry python && \
    cd /usr/local/bin && \
    ln -s /opt/poetry/bin/poetry && \
    poetry config virtualenvs.create false

COPY ./backend/app/pyproject.toml ./backend/app/poetry.lock* /app/

RUN poetry install --no-root --no-dev

COPY ./backend/app /app

COPY --from=frontend-build-stage /app/dist /app/static

ENV PYTHONPATH=/app
