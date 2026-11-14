# 11/14 report 지시 ① 전날 작업별 출력 토큰 ② start_calc < calc_complete 진단

## ① 토큰 (도구 work/tokenday.py — 매일 report 회차가 돌림)
### 2026-11-13 작업별 출력 토큰 (세션 jsonl 합, 측정 11-14 12:39)
| 작업 | 회차 | 출력 토큰 | 비중 | 커밋(결과물) |
|---|---|---|---|---|
| firemap-video-producer | 6 | 239,563 | 30% | 6 |
| firemap-write-b | 6 | 145,281 | 18% | 5 |
| firemap-write | 6 | 144,456 | 18% | 7 |
| firemap-visual-designer | 2 | 48,819 | 6% | 2 |
| pc-health-guard | 23 | 40,835 | 5% | 0 |
| 나머지 11종 | 20 | 172,540 | 21% | - |
| 합계 | 63 | 791,494 | | 커밋 34 |
- 11/12 300만 → 11/13 79만(쉼 ①~④ 효과). PD 30%로 1위(렌더 메모리 부족 재시도), 쉼 순서 근거: PD·write-b·write가 66%. PC 감시는 23회지만 5%.
- 결과물 수 = 그날 커밋 중 작업 머리말(pd·write·write-b·visual 등) 수. 커밋 없는 작업(PC 감시)은 0으로 나옴.

## ② start_calc < calc_complete (진단만, 고치지 않음 — 10/6 사이트 개발 중단)
- 측정 12:39, Supabase firemap_events 7일: calc_complete 43건·18명 / start_calc 18건. 18명 중 16명(89%)은 start_calc도 있음, 7일 전부터 있던 재방문 3명, 시작 없이 완료만 2명.
- 원인(코드): start_calc는 홈 '시작' 버튼 한 곳(src/components/firemap/Home.jsx:54)에서만 찍힘. calc_complete는 결과 화면이 뜰 때마다 찍힘(Result.jsx:148, useEffect [inputsHash]) — 저장된 입력으로 결과 다시 열기·메뉴 '내 파이어 결과'·바꿔보기/랭킹/메뉴에서 돌아오기·월급/퇴직금/실업급여/대출 계산기가 result로 보낼 때 모두 다시 찍힘. 그래서 1명당 평균 2.4건.
- 결론: 건수 비율은 이탈률이 아님. **사람(client_id) 기준으로 재면 시작→완료 16/18**. 이탈률은 client_id 고유 수로 잰다.
