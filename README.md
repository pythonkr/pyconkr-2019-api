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

# Pycon KR Web 구조
- Frontend 는 React 자바스크립트 라이브러리를 사용하여 사용자가 보는 화면의 구조를 생성한다.
- Backend 는 django 프레임웍을 사용하여 개발한다.
- 동적인 데이터는 GraphQL 을 통해 조회하여 클라이언트 브라우져에서 완성하도록 한다.
- SSR(Server Side Rendered) 를 위해 NEXT.js 를 사용한다. (?)

## 부록
- Frontend github : https://github.com/pythonkr/pyconkr-web
- Backend github : https://github.com/pythonkr/pyconkr-api
- 빠른 이해를 위한 간단한 설명 나열

### React
- React 자체를 이해하기 위해서는 많은 시간이 소요됨
- 문법 자체에 대한 적당한 이해가 되었다면 구현 튜토리얼을 먼저 이해한 뒤 다시 문법을 파악하는 것이 도움이 될 수 있음

#### 참고 링크
- React 공식 페이지 : https://reactjs.org
- React 위키 백과 : https://ko.wikipedia.org/wiki/리액트_(자바스크립트_라이브러리)#JSX
- React 한글 튜토리얼 추천 : https://velopert.com/3613
- React 의 실제 구현 튜토리얼 추천 : http://ibrahimovic.tistory.com/32?category=711523
- JSX 튜토리얼 : https://velopert.com/3626


### django
- python 으로 만들어진 무료 오픈소스 웹 어플리케이션 프레임워크

#### 참고 링크
- django 공식 페이지 : https://www.djangoproject.com
- django 한글 튜토리얼 추천 : https://tutorial.djangogirls.org/ko/django/


### GraphQL
- 페이스북이 발표한 데이터 질의어

#### 참고 링크
- GraphQL 개념 : https://velopert.com/2318
- GraphQL + django : http://docs.graphene-python.org/projects/django/en/latest/


### NEXT.js
- Zeit.co 팀에 의해 발표된 React JS를 이용한 서버 사이드 렌더링 프레임워크 (SSR, Server Side Rendering)

#### 참고 링크
- next.js 공식 페이지 : https://nextjs.org
-next.js 한글 튜토리얼 추천 : https://velopert.com/3293
