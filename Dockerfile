FROM python:3.10-buster

WORKDIR /app

RUN pip install pipenv
COPY src/Pipfile.lock /app
COPY src/Pipfile /app
RUN pipenv install --system --deploy --ignore-pipfile

COPY src/ /app

USER 1000:1000