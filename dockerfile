FROM python:3.9-slim-buster

WORKDIR /pme

COPY ./app/requirements.txt ./pme/requirements.txt

RUN pip install --no-cache-dir --upgrade -r ./pme/requirements.txt

COPY ./app /pme/