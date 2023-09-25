FROM python:3.11-alpine3.18

WORKDIR /backend

COPY requirements.txt /temp/requirements.txt

EXPOSE 8000

RUN pip install -r /temp/requirements.txt

COPY . .