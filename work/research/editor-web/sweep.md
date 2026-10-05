# 화면 문구 전수 점검 목록 (firemap-editor-web)
근무마다 '다음 칸'부터 이어서 본다. 기준: 메모리 firemap-korean-copy(내 말 짓지 않기, 같은 말 두 번 금지) · 사실·숫자·법정 문구·면책은 불변.
표시: ✅ 봄(고침 n) · ⏳ 다음 · — 대상 아님

| # | 화면 | 파일 | 상태 | 메모 |
|---|---|---|---|---|
| 1 | 연봉 실수령 /calc/salary | src/components/firemap/SalaryCalc.jsx | ✅ 10/1 08:30 (2곳) | 중복 문장 2개 삭제(연말정산 문장이 결과 카드·면책 두 번, 생활비 설명이 버튼 아래·생활비 카드 두 번) |
| 2 | 퇴직금 /calc/severance | src/components/firemap/SeveranceCalc.jsx | ✅ 10/1 (0곳) | 용어 고용노동부 그대로. 남은 점: 결과 카드 sub '재직 N일'과 타일 '재직일수 N일'이 같은 숫자 → 디자이너에게 넘김(구조 문제) |
| 3 | 실업급여 /calc/unemployment-benefit | src/components/firemap/UnemploymentCalc.jsx | ✅ 10/1 (0곳) | 은퇴 연결 제목·설명은 bc7b7e5에서 법(제40조) 근거로 일부러 바꾼 것 — 되돌리지 않음 |
| 4 | 쿠팡 칸 | CoupangPick.jsx · firemap-v2/coupangPicks.js | ✅ 10/1 (0곳) | 대가성 문구는 법정 권장 문구 그대로. 상품 3개 모두 null(아직 안 보임) → 상품 들어오면 title·desc 다시 본다 |
| 5 | 키트 /kit/demo | public/kit/demo/index.html | — | 영어 내부 테스트(noindex) → firemap-editor-en |
| 6 | 홈 | Home.jsx | ✅ 10/1 13:30 (2곳) | 근거 없는 꾸밈말 '현실적인' 삭제, 번역투 '당신은'→히어로 제목과 같은 '나는 …할까?' |
| 7 | 질문 | Question.jsx · firemap-v2/data.js questions | ✅ 10/1 (0곳) | |
| 8 | 결과 | Result.jsx | ✅ 10/1 (0곳) | |
| 9 | 배당 생활 계산 | DividendLifeCalc.jsx | ✅ 10/1 (0곳) | |
| 10 | 건보 피부양자 | DependentCheck.jsx | ✅ 10/1 (0곳) | 법정 기준 문장 그대로 |
| 11 | 세금·연금 | TaxPensionModules.jsx · PensionControls.jsx | ✅ 10/1 (0곳) | |
| 12 | 해외 체류 | OverseasStayModule.jsx · CityExplorer.jsx | ✅ 10/1 (1곳) | 지역 자료 링크 설명이 제목과 같은 말 → 그 페이지 meta '144개 조합의 필요자산·저축 플랜' |
| 13 | 파이어 유형 테스트 | FireTypeTest.jsx · firemap-v2/cityTypeTest.js | ✅ 10/1 (4곳) | 오타 '줄여보요', '핵심이에요', '설계하면…확 줄어요'(같은 카드 '확 줄어요' 두 번), '현실파'+'가장 현실적' 반복. 2c9e93e 운영 반영 |
| 14 | 랭킹·벽·실험 | Leaderboard.jsx · Wall.jsx · Experiment.jsx | ✅ 10/1 18:35 (1곳) | 바꿔보기 요약 '연봉 N%'↔칸 이름 '임금상승률' → '임금'으로 하나(fb99c58 운영). funName.js '현명한'은 닉네임 형용사라 aitell 오탐 — 안 바꿈(바꾸면 기존 사용자 닉네임이 바뀜) |
| 15 | 커뮤니티·뉴스 | Community.jsx · News.jsx · CafePoster.jsx | ✅ 10/1 18:45 (2곳) | 다시 시도 안내를 앱 다수 '잠시 후 다시 해봐요'로(b57ac17 운영). CafePoster는 운영자 전용 화면이라 안 봄.  firemap-v2/cafePosts.js는 발행된 카페 글 사본(aitell 6건) — 원본과 어긋나면 안 돼서 firemap-editor 소관, 여기선 안 고침 |
| 16 | 공유·계정·설정·동의 | ShareSheet.jsx · AccountCard.jsx · Settings.jsx · Consent.jsx · MenuAll.jsx | ✅ 10/2 13:30 (2곳) | Settings 저장 실패 토스트 '잠시 후 다시 눌러주세요'→앱 기준 '잠시 후 다시 해봐요'. AccountCard 로그인 설명 '카카오로 3초면 돼요' 삭제(잰 적 없는 숫자). Consent는 면책 성격이라 그대로. Settings의 브라우저 조작 안내 '~주세요'는 행동 지시라 그대로 |
| 17 | 셸·메뉴 | FireMapMVP.jsx · src/ui/* | ✅ 10/5 20:10 (0곳) | 토스트·카운트다운·입력 칸 안내 모두 짧은 해요체, 같은 말 반복 없음 |
| 18 | 푸시 알림 | firePush.js · public/sw.js · supabase/functions/send-fire-clock | ✅ 10/5 20:10 (1곳) | 실제 문구는 엣지함수에. 기본 문구가 '…확인해보세요 — 확인하기'로 '확인' 두 번 → 꼬리 뺌(b3d54a6). **엣지함수 배포 전엔 라이브에 안 반영**(git push로 안 올라감) |
| 19 | 검색용 본문 | functions/_middleware.js · firemap-v2/toolPages.js | ✅ 10/5 20:10 (1곳) | 도구 블록에 '1분이면 나도 계산'이 부제·링크 두 번 → 링크를 앱 말 '파이어맵 홈'(TopBar aria-label)로(b3d54a6 운영). toolPages 설명·본문은 화면 라벨·법 조문이라 그대로. 홈 블록 35·36줄은 index.html description·JSON-LD 원문 사본이라 그대로 |
| 20 | 메타 | index.html | ✅ 10/5 (0곳) | description·JSON-LD 짧고 사실. og 태그는 index.html에 없음(미들웨어가 넣음) |
| 21 | 안내 페이지 | public/*.html(contact·disclaimer·privacy·insights·fire-jok) | ⏳ 다음 | 면책·개인정보는 법정 문구 불변 |
| 22 | 가이드 101편 | public/guide/*.html(생성기 work/gen-guides.mjs) | ⏳ | 생성기 원본에서 고친다 |
| 23 | 공유 카드 이미지 글자 | functions/og*.js | ⏳ | |
