# PyCon.KR api

[![CircleCI](https://circleci.com/gh/pythonkr/pyconkr-api.svg?style=svg)](https://circleci.com/gh/pythonkr/pyconkr-api) [![codecov](https://codecov.io/gh/pythonkr/pyconkr-api/branch/master/graph/badge.svg)](https://codecov.io/gh/pythonkr/pyconkr-api)

A git repository for PyCon Korea api.

## Requiremensts

- Python 3.6.3

## Getting started

```bash
$ git clone git@github.com:pythonkr/pyconkr-api.git
$ cd pyconkr-api
$ make up
```

## How to run with docker-compose

다음 명령어로 배포가 가능합니다.

```
$ export DJANGO_SETTINGS_MODULE=pyconkr.staging_settings 
$ docker-compose up -d --build --force-recreate
```

## Contribution

처음 Contribution를 하시는 분이라면, Pull Request를 만들기 전에 [Contribution Guide](.github/CONTRIBUTING.md)를 꼭 읽어주세요.
