FROM python:3.11.4-slim-buster

ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1

WORKDIR /app

COPY requirements.txt /app/

RUN python -m pip install --upgrade pip
RUN pip install -r requirements.txt

COPY ./core /app/