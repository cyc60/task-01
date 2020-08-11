FROM python:3.8-slim-buster

ADD ./src /srv/src

WORKDIR /srv/src

RUN pip3 install -r requirements.txt

EXPOSE 8000