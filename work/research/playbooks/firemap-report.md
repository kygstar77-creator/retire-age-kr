- 10/6: growth 예약이 지워지면 수익 일지가 끊긴다 — report 회차가 revenue_daily.py --set(쿠팡 크롬 홈 '이번 달 집계'·애드센스 u/2 사이트 목록, 표가 늦게 떠서 5초 기다린 뒤 확대 캡처) + sitedaily.sql 날짜만 바꿔 한 줄. 손으로 시각 쓸 땐 date 값만(12:4x라 미리 적었다가 고침).

- 2026-10-08: 모든 회차 시작 시각이 같으면(12:55 동시) 재부팅 신호다. 빵꾸를 보면 먼저 Get-WinEvent System Id 6008로 꺼진 구간을 재고, 이미 도는 write·watchdog가 있으면 report는 보충 발행하지 않는다(중복 위험). runs_today.json의 date가 어제면 work/runs/<그 날짜>.json으로 보관한다(오늘 날짜로 복사 금지).
- 2026-10-09 report: '클릭 0'은 먼저 운영 화면(?fm_internal=1)에서 직접 눌러 firemap_events(ts 칼럼, created_at 아님)에 internal 줄이 찍히는지 본다 — 찍히면 원인은 안 누름. 브라우저 패널은 새 탭(쿠팡)을 막지만 onClick 기록은 나간다. 크롬 쿠팡 파트너스 리포트는 해시 주소로 열면 숫자 없이 빈 화면으로 읽힐 때가 있다.
