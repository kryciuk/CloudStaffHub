FROM python:3.10.9-slim AS builder

RUN apt-get update \
	&& apt-get -y install gcc \
	&& rm -rf /var/lib/apt/lists/*

# DEVELOPMENT
ENV \
	PIP_NO_CACHE_DIR=off \
	PIP_DISABLE_PIP_VERSION_CHECK=on \
	PYTHONDONTWRITEBYTECODE=1 \
	PYTHONUNBUFFERED=1 \
	VIRTUAL_ENV=/pybay-venv \
	POETRY_VIRTUALENVS_CREATE=false \
	POETRY_VIRTUALENVS_IN_PROJECT=false \
	POETRY_NO_INTERACTION=1 \
	POETRY_VERSION=1.8.3

RUN pip install "poetry==$POETRY_VERSION"

COPY poetry.lock pyproject.toml ./

ENV PATH="$VIRTUAL_ENV/bin:$PATH"

# Install python packages
RUN python -m venv $VIRTUAL_ENV \
	&& . $VIRTUAL_ENV/bin/activate \
	&& poetry install

WORKDIR /CloudStaffHub

RUN poetry install

COPY . .




#
#FROM python:3.10.9 AS builder
#
#RUN apt-get update \
#	&& apt-get -y install gcc \
#	&& rm -rf /var/lib/apt/lists/*
#
## DEVELOPMENT
#ENV \
#	PIP_NO_CACHE_DIR=off \
#	PIP_DISABLE_PIP_VERSION_CHECK=on \
#	PYTHONDONTWRITEBYTECODE=1 \
#	PYTHONUNBUFFERED=1 \
#	VIRTUAL_ENV=/pybay-venv \
#	DB_NAME="CloudStaffHub" \
#	DB_USER="postgres" \
#	DB_PASSWORD="Kefiros1!" \
#	DB_HOST="127.0.0.1" \
#	DB_PORT="5432" \
#	SMTP_HOST="django.testing.klaudia@gmail.com" \
#	SMTP_PASSWORD='ewlg pnkh maki wjxr'
#ENV \
#	POETRY_VIRTUALENVS_CREATE=false \
#	POETRY_VIRTUALENVS_IN_PROJECT=false \
#	POETRY_NO_INTERACTION=1 \
#	POETRY_VERSION=1.8.3
#
#RUN pip install "poetry==$POETRY_VERSION"
#
#COPY poetry.lock pyproject.toml ./
#
#ENV PATH="$VIRTUAL_ENV/bin:$PATH"
#
## Install python packages
#RUN python -m venv $VIRTUAL_ENV \
#	&& . $VIRTUAL_ENV/bin/activate \
#	&& poetry install
#
#WORKDIR /CloudStaffHub
#
#RUN poetry install
#
#COPY src/ .
#
#EXPOSE 8000
#
#CMD python manage.py runserver
