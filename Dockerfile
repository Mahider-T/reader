# syntax=docker/dockerfile:1

FROM python:3.11.4-alpine3.18

WORKDIR /app

COPY . /app

RUN pip3 install -r requirements.txt

COPY . .

CMD [ "flask", "--app" , "flaskr", "run"]