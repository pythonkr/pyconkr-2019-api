# 파이콘 한국 Contributing Guide

Contributor 여러분 안녕하세요!!
pyconkr-api contribution을 제출할 때에는 반드시 다음 가이드라인을 따라주세요.

- [PyCon.KR Web Structure](#pyconkr-web-structure)
- [Pull Request Guidelines](#pull-request-guidelines)
- [Commit Checklist](#commit-checklist)
- [Knowledge](#knowledge)
- [Reference](#reference)

## PyCon.KR Web Structure

파이콘 한국 Webpage는 [frontend](https://github.com/pythonkr/pyconkr-web)와 [backend](https://github.com/pythonkr/pyconkr-api)로 구성되어 있습니다.

- Frontend 는 React 자바스크립트 라이브러리를 사용하여 사용자가 보는 화면의 구조를 생성합니다.
- Backend 는 django 프레임워크을 사용하여 개발합니다.
- 동적인 데이터는 GraphQL 을 통해 조회하여 클라이언트 브라우져에서 완성하도록 합니다.
- SSR(Server Side Rendered) 를 위해 NEXT.js 를 사용합니다. (수정 필요)


## Pull Request Guidelines

- `develop`
  - contribution을 할 때에는 `develop`에서 관련 branch를 생성해서 작업을 해주세요.
  - 관련 branch 이름은 다음 규칙을 따를 것을 권장합니다.
    1. 기능 추가/개선: feature/\*
    2. 버그 픽스: bugfix/\*
    3. 문서 개선: doc/\*
- `master`
  - **관리자 외에는 master에 merge하는 PR을 만들지 말아주세요**
  - master branch에는 **배포 가능한 안정된 snapshot**이 들어가야 합니다.
- `release`
  - **관리자 외에는 release에 merge하는 PR을 만들지 말아주세요**
  - release branch는 **2019년 티쳐 페이지를 오픈할 때에 생성**할 예정입니다.
  - 이 branch에 변화가 생기면 모두 공개 페이지에 반영됩니다.

## Commit Checklist

다음 사항들을 확인하고 코드를 커밋해주세요.

1. pylint를 준수했는지 여부
   - 여러분이 pylint 관련 플러그인이 있는 IDE를 사용한다면 세이브할때마다 에러를 쉽고 빠르게 확인할 수 있습니다.
2. 추가한 기능의 테스트 케이스를 작성했는지 여부
   - 자동화된 테스트는 자동화된 베포를 가능하게 합니다 :)
3. 코드를 삭제하지 않고 주석으로 처리해두진 않았는지
   - 꼭 필요한 코드였다면 VCS의 기능을 활용하는 것이 더 좋습니다.
4. 설치한 패키지를 `requirements.txt`에 반영했는지
   - 추가하지 않으면 CI나 베포 환경에서 에러가 발생하게 됩니다.
   ```bash
   $ pip freeze > requirements.txt
   ```

## Knowledge

1. GraphQL
    - 페이스북이 발표한 데이터 질의어

## Reference

- GraphQL 공식 페이지 : https://graphql.org
- GraphQL + django : http://docs.graphene-python.org/projects/django/en/latest/
