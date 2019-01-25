# 파이콘 한국 Contributing Guide

Contributor 여러분 안녕하세요!!
pyconkr-api로 contribution을 시작하거나 제출하기 전에 다음 가이드라인을 읽고 따라주세요.

- [Pull Request Guidelines](#pull-request-guidelines)
- [Commit Checklist](#commit-checklist)

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
