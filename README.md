# PyCon.KR api

[![CircleCI](https://circleci.com/gh/pythonkr/pyconkr-api.svg?style=svg)](https://circleci.com/gh/pythonkr/pyconkr-api) [![codecov](https://codecov.io/gh/pythonkr/pyconkr-api/branch/master/graph/badge.svg)](https://codecov.io/gh/pythonkr/pyconkr-api)

A git repository for PyCon Korea api.

## PyCon.KR Web 구조

- Frontend 는 React 자바스크립트 라이브러리를 사용하여 사용자가 보는 화면의 구조를 생성한다.
- Backend 는 django 프레임워크을 사용하여 개발한다.
- 동적인 데이터는 GraphQL 을 통해 조회하여 클라이언트 브라우져에서 완성하도록 한다.
- SSR(Server Side Rendered) 를 위해 NEXT.js 를 사용한다. (?)

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

## 부록
- Frontend github : https://github.com/pythonkr/pyconkr-web
- Backend github : https://github.com/pythonkr/pyconkr-api
- 빠른 이해를 위한 간단한 설명 나열

### GraphQL
- 페이스북이 발표한 데이터 질의어

#### 참고 링크
- GraphQL 공식 페이지 : https://graphql.org
- GraphQL + django : http://docs.graphene-python.org/projects/django/en/latest/



