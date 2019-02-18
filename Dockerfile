 FROM python:3.6.3
 ENV PYTHONUNBUFFERED 1
 RUN mkdir /config
 ADD requirements.txt /config/
 WORKDIR /config
 RUN pip install -r requirements.txt
 RUN mkdir /web
 WORKDIR /web