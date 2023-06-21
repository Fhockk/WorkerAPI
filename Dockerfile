FROM python:3.9-slim-buster

RUN apt-get update && apt-get install -y \
    gcc \
    python3-dev \
    libpq-dev

WORKDIR /meduzzen

COPY requirements.txt requirements.txt
RUN pip install -r requirements.txt

COPY . .
