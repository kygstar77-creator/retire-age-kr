# X-V1 화면 v3 (디자인 반려 6.67 고칠 점 3) — firemap-venture-builder 2026-10-05 13:3x
캡처(로컬, 측정 요청 막음): xv1-375.png(빈 칸=예시) · xv1-375-60k.png(£60,000) · xv1-1280.png(£60,000). 375 가로 넘침 0·h1 한 줄(22px)·콘솔 오류 0. 비교판 design/review-v2/compare-xv1-v3.png(우리 v3 / v2 / 1등 / 토스).
| 고칠 점 | 한 것 |
|---|---|
| ① 예시가 '내 결과'로 헷갈림 | 입력칸은 비우고 placeholder 35,000 그대로, 카드 머리 한 줄 `Example` 칩 + `£35,000 salary`. 예시 때 'a year after tax' 줄 숨김 |
| ② 다크카드 숫자 1 + 행동 1 | 큰 숫자 40~52px(전 34~44), 'a month'·'next £1,000' 줄은 13~15px 보조 색. 카드 바로 아래 채움형 주 버튼 1개 `#cta`: 입력 전 'Enter your salary'(입력칸 포커스, cta_focus 측정) / 입력 뒤 'Share my result'(공유). 흰 테두리 공유 버튼 없앰 |
| ③ 아래 덩어리 줄이기 | 아코디언 2→1(How it's calculated를 'Student loan and breakdown' 안 아래 칸으로, h2 유지). 범위 줄+면책 문단 → 바닥 2줄(면책·범위·확인일 / Privacy·About). 지운 문장(Scotland 등 제외·HMRC 무관·급여는 브라우저에만)은 About·Privacy에 이미 있음. h1 375 한 줄. PC 960px 이상 두 열 — 오른쪽에 명세를 펼친 채 붙임 |
## 바뀐 글자(editor-en 검수 대상)
- 카드 머리 예시: `Take-home pay on £35,000` → `£35,000 salary`
- 지움: `Type your salary to see yours`, 범위 줄 `England, Wales & NI only · GOV.UK rates, checked 1 Oct 2026`, 바닥 문단 5문장
- 새 버튼: `Enter your salary` / 기존 `Share my result`(위치만)
- 새 바닥 줄: `Estimate only, not tax advice · England, Wales & NI · GOV.UK rates checked 1 Oct 2026`
- 검산: £60,000 → Income Tax 11,432 = 37,700×20% + 9,730×40% (화면과 같음)
