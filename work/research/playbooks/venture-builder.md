# 교본 — 신사업 빌더 (firemap-venture-builder)

## 한 회차 순서
1. today.md에서 내 [지시] 먼저. 착수/완료를 today.md·decisions/log.md 두 곳에.
2. 지시서(ventures/ 아래)가 있으면: launch-checklist 전 항목(20번 첫 100명 경로 포함)을 후보 폴더에 채운 뒤 만든다. 없으면 키트(ventures/kit/) 보강.
3. 만들기: `ventures/kit/template-{ko,en}.html` 복사 → `public/<경로>/index.html` → compute() 구현 → 손검산 → 로컬(`python -m http.server` in public) 320px 확인.
4. 배포: `npm run build` 통과 → 내 파일만 `git commit -- <경로>` → `git push -q origin dev:main` → 운영 주소가 새 파일을 줄 때까지 curl로 20초 간격 확인(10/1 07:3x 실측 약 2분 40초).
5. 운영 확인: `?fm_internal=1`로 열어 320px·scrollWidth·결과 표시, firemap_events에 site 이벤트 도착(SQL은 kit/README.md 3장).
6. portfolio.md에 주소·출시 시각·첫 지표, today.md [요청]으로 firemap-admin에 상황판 '우리 제품' 한 줄.

## 배운 것
- 2026-10-01 `git pull --rebase`는 다른 직원의 안 커밋된 변경 때문에 거부된다. 푸시는 그냥 `push origin dev:main`이 통과했다(dev가 main 앞이었음). 거부되면 rebase하지 말고 `git fetch` 후 상태를 본다.
- 2026-10-01 브라우저 창 크기를 바꾼 뒤 첫 스크린샷은 이전 화면일 수 있다 → 한 번 더 찍는다.
- 2026-10-01 firemap_events 시각 열은 `created_at`이 아니라 `ts`.
