FROM python:3.6.3

ENV PYTHONUNBUFFERED 1
WORKDIR /config
ADD requirements.txt /config/
RUN pip install -r requirements.txt

WORKDIR /web
ENTRYPOINT ["/web/docker-entrypoint.sh"]