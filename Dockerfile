FROM python:3

COPY . /app
WORKDIR /app

RUN python ./main.py
