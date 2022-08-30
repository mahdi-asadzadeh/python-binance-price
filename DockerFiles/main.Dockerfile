FROM python:3.10
LABEL MAINTAINER="Mahdi Asadzadeh | mahdi.asadzadeh.programing@gmail.com"

ENV PYTHONUNBUFFERED 1

RUN mkdir /app
WORKDIR /app
COPY main.py /app

COPY requirements.txt /app/

RUN pip install --upgrade pip
RUN pip install -r requirements.txt
