FROM python:latest

WORKDIR /app

RUN apt update && \
    apt upgrade -y && \
    apt install -y docker.io

COPY . .

RUN pip install -r requirements.txt

ENTRYPOINT python tdp.py