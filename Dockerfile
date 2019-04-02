FROM python:3.6.8-stretch

ENV PYTHONUNBUFFERED 1
WORKDIR /config

RUN apt-get update && apt-get install -y cron
RUN service cron start

ADD requirements.txt /config/
RUN pip install -r requirements.txt

WORKDIR /web
ENTRYPOINT ["/web/docker-entrypoint.sh"]