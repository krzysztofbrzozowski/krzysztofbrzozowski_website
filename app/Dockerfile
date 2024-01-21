# Use latest Python image
FROM python:3.12.1-alpine3.19

ENV PYTHONUNBUFFERED 1


COPY ./requirements.txt /requirements.txt
COPY ./requirements.dev.txt /requirements.dev.txt

# DEVELOPMENT FLAG
ARG DEV=false

# Install all packages
RUN python -m venv /py && \
    /py/bin/pip install --upgrade pip && \
    apk add --update --no-cache postgresql-client bash

RUN pip install -r /requirements.txt && \
      if [ $DEV = "true" ]; \
        then pip install -r /requirements.dev.txt ; \
      fi

# RUN apk del .tmp-build-deps

COPY . /app

WORKDIR /app
RUN adduser -D django_user
USER django_user