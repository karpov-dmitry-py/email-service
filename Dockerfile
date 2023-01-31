FROM python:2.7.18

ENV PYTHONUNBUFFERED 1

COPY ./requirements.txt ./
RUN pip install --no-cache-dir -r /requirements.txt

RUN mkdir /app
COPY ./emailer /app
WORKDIR /app