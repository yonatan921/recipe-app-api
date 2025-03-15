FROM python:3.9-alpine3.13
LABEL maintainer="ybaruch"

ENV PYTHONUNBUFFERED=1

# ✅ Install SSL certificates before switching users
RUN apk update && apk add --no-cache ca-certificates

COPY ./requirements.txt /tmp/requirements.txt
COPY ./requirements.dev.txt /tmp/requirements.dev.txt
COPY ./app /app

WORKDIR /app
EXPOSE 8000

ARG DEV=false
RUN python -m venv /py && \
    /py/bin/pip install --upgrade pip && \
    apk add --update --no-cache postgresql-client && \
    apk add --update --no-cache --virtual .tmp-build-deps \
    build-base postgresql-dev musl-dev && \
    /py/bin/pip install -r /tmp/requirements.txt && \
    if [ "$DEV" = "true" ]; then \
      /py/bin/pip install -r /tmp/requirements.dev.txt; \
    fi && \
    rm -rf /tmp && \
    apk del .tmp-build-deps && \
    adduser --disabled-password --no-create-home django-user && \
    chown -R django-user:django-user /app

# Ensure the correct Python path and settings module
ENV PATH="/py/bin:$PATH"
ENV PYTHONPATH=/app
ENV DJANGO_SETTINGS_MODULE=app.settings

USER django-user
