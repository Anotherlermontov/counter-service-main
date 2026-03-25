FROM python:3.11-slim-bookworm

ARG UID=800
ARG GID=800
ARG APP_PORT=8000

ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    RUN_USER=app \
    RUN_GROUP=app \
    APP_DIR=/opt/app

RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential \
    libpq-dev \
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/*

RUN groupadd -g ${GID} -o ${RUN_GROUP} && \
    useradd -m -u ${UID} -g ${GID} -o ${RUN_USER}

RUN python -m pip install --upgrade pip

COPY --chown=${RUN_USER}:${RUN_GROUP} . ${APP_DIR}
WORKDIR ${APP_DIR}

RUN pip install -r requirements.txt --no-cache-dir --no-deps --require-hashes

EXPOSE $APP_PORT

CMD ["python", "manage.py", "runserver", "0.0.0.0:8000"]
