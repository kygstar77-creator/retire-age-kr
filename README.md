# 퇴사나이

한국 직장인이 몇 살에 회사를 그만둬도 되는지 판단하는 React + Vite 기반 조기은퇴/반퇴 시뮬레이터입니다.

## 실행 방법

```bash
npm install
npm run dev
```

개발 서버가 실행되면 터미널에 표시되는 로컬 주소를 브라우저에서 열면 됩니다. 보통 `http://localhost:5173` 입니다.

## 빌드

```bash
npm run build
```

Cloudflare Pages 배포용 정적 파일을 만들 때는 아래 명령을 사용합니다.

```bash
npm run build:deploy
```

`wrangler.json`에 Cloudflare Pages 설정이 있어, GitHub 저장소를 연결하면 `.github/workflows/pages.yml`이 `outputs/deploy` 폴더를 자동 배포합니다.

## 주요 기능

- 목표 퇴사 나이 기준 자산 고갈 나이 계산
- 사용자가 입력한 종료 나이까지 금융자산이 고갈되지 않는 가장 빠른 퇴사 가능 나이 계산
- 목표 퇴사 나이에서 1년, 2년, 3년 더 근무하는 시나리오 비교
- 국민연금 수령 전 공백기 해석
- 입력값 localStorage 자동 저장
- 초기화 버튼 제공
