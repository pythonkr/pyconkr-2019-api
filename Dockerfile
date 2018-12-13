 FROM python:3.6.3
 ENV PYTHONUNBUFFERED 1
 RUN mkdir /web
 WORKDIR /web
 ADD requirements.txt /web/
 RUN pip install -r requirements.txt
 ADD . /web/