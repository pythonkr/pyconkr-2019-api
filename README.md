# PyCon.KR api

[![CircleCI](https://circleci.com/gh/pythonkr/pyconkr-api.svg?style=svg)](https://circleci.com/gh/pythonkr/pyconkr-api) [![codecov](https://codecov.io/gh/pythonkr/pyconkr-api/branch/master/graph/badge.svg)](https://codecov.io/gh/pythonkr/pyconkr-api)

A git repository for PyCon Korea api.

## Requiremensts

- Python 3.6.3

## Getting started

설치하거나 도커를 활용하여 postgresql을 설치합니다.

```sh
$ docker run -d --name postgres -p 5432:5432 postgres

```

그리고 서비스를 구동합니다.


```bash

$ git clone git@github.com:pythonkr/pyconkr-api.git
$ cd pyconkr-api 

$ ./manage.py migrate
$ ./manage.py runserver
```


## Contribution

처음 Contribution를 하시는 분이라면, Pull Request를 만들기 전에 [Contribution Guide](.github/CONTRIBUTING.md)를 꼭 읽어주세요.


## 2024 Frozen

I made builded docker file for prod

```
docker build -f DockerfileProd -t {AWS_ID}.dkr.ecr.ap-northeast-2.amazonaws.com/{CLUSTER_NAME}/{APP_ID}:prod_frozen .
```

