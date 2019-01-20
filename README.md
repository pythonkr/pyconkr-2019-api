# pyconkr-api

[![CircleCI](https://circleci.com/gh/pythonkr/pyconkr-api.svg?style=svg)](https://circleci.com/gh/pythonkr/pyconkr-api) [![codecov](https://codecov.io/gh/pythonkr/pyconkr-api/branch/master/graph/badge.svg)](https://codecov.io/gh/pythonkr/pyconkr-api)

A git repository for PyCon Korea api.

## Requiremensts

- Python 3.6.3

## Getting started

```bash
$ git clone git@github.com:pythonkr/pyconkr-api.git
$ cd pyconkr-api
$ pip install -r requirements.txt
$ python manage.py makemigrations
$ python manage.py migrate
$ python manage.py runserver
```

## For developer

When installing additional pip packages, please reflect in requirements.txt.

```bash
$ pip freeze > requirements.txt
```
