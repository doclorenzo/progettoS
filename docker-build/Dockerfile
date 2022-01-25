FROM python:3.8-slim-buster

WORKDIR /app
COPY requirements.txt requirements.txt
RUN python3 -m pip install -r requirements.txt

ENV MYSQL_USER root
ENV MYSQL_PASSWORD vvs
ENV MYSQL_HOST mysql
ENV MYSQL_DB laureati2

COPY . .

CMD python3 flask0s.py
