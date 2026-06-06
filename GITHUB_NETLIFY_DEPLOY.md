# GitHub + Netlify 자동 배포 안내

이 방식으로 바꾸면 zip을 매번 직접 올리지 않아도 됩니다.
코드를 GitHub에 올리고 Netlify 프로젝트를 GitHub 저장소에 연결하면, 이후 변경사항이 올라갈 때마다 Netlify가 자동으로 새 버전을 배포합니다.

## 1. GitHub 저장소 만들기

1. GitHub에 로그인합니다.
2. 새 저장소를 만듭니다.
3. 저장소 이름은 예를 들어 `retire-age-kr`로 둡니다.
4. 이 프로젝트 폴더의 파일들을 GitHub 저장소에 올립니다.

## 2. Netlify에서 GitHub 연결하기

1. Netlify 프로젝트로 들어갑니다.
2. `Project configuration` 또는 `Build & deploy` 메뉴로 갑니다.
3. `Link repository`, `Connect Git repository`, `Continuous deployment` 중 비슷한 버튼을 누릅니다.
4. GitHub를 선택합니다.
5. `retire-age-kr` 저장소를 선택합니다.

## 3. Netlify 빌드 설정

이 프로젝트에는 `netlify.toml` 파일이 있어서 보통 자동으로 잡힙니다.

- Build command: `npm run build:deploy`
- Publish directory: `outputs/deploy`

Netlify 화면에서 이 값이 비어 있거나 다르게 나오면 위 값으로 맞추면 됩니다.

## 4. 다음부터 배포하는 법

코드를 수정한 뒤 GitHub에 올리면 Netlify가 자동으로 배포합니다.
수동 zip 업로드는 더 이상 필요하지 않습니다.

## 주의

현재 앱은 서버, 로그인, DB 없이 브라우저에서만 계산합니다.
사용자가 입력한 값은 각 사용자 브라우저의 localStorage에만 저장됩니다.
