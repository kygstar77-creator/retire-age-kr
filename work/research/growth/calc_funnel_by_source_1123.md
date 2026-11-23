# 유입처별 계산 완주 — 11/1~11/23 12:5x (firemap-report, 회의 11/22 21:43 지시②)
출처: Supabase firemap_events(c7cd8a90). 기기(client_id) 단위, 첫 session_start의 utm_source → 없으면 ref 호스트 → 없으면 direct. bot 표시 기기 뺌.
'완주' = calc_complete(홈 '/' 은퇴 나이 계산기) 또는 calc_result(연봉·퇴직금·실업급여).

| 유입처 | 기기 | 계산 완주 | 쿠팡 이벤트 | 랜딩 |
|---|---|---|---|---|
| direct | 169 | 26 | 0 | / 외 여러 곳 |
| youtube(utm) | 44 | 0 | 1(보기) | / · /calc/salary · /dividend |
| m.dcinside.com | 8 | 8 | 0 | / |
| **cafe(utm)** | **8** | **0** | 0 | /health-insurance 6 · /dividend 2 · /calc/unemployment-benefit 1(기기 중복 있음) |
| pwa | 5 | 1 | 0 | / |
| google | 4 | 2 | 0 | / |
| theqoo | 3 | 3 | 0 | / |
| 다음카페 | 3 | 2 | 0 | / |
| 네이버 검색 | 2 | 2 | 0 | / |
| 기타(chatgpt·toss·youtube.com·bing) | 4 | 3 | 0 | / |

## 카페에서 온 사람이 왜 계산을 안 '시작'하나 — 실측으로 확인한 것
- **측정이 없다**: 10/1~11/23 계산 이벤트(calc_complete·start_calc·calc_input_start·calc_result)를 내는 화면은 홈 '/'(firemap)·연봉·퇴직금·실업급여 4곳뿐. **/dividend·/health-insurance(화면 dependent)는 계산 이벤트를 한 건도 안 낸다** → 카페 8기기 중 7기기가 간 화면은 계산을 해도 0으로 찍힌다. 'cafe 0/8'은 완주율이 아니라 측정 빈칸.
- 측정되는 곳으로 간 카페 기기는 1대(/calc/unemployment-benefit, screen_view 1 뒤 이벤트 없음) — 표본 1이라 원인 판단 못 함.
- 대조: '/'로 들어온 외부 유입(디시·theqoo·다음카페·네이버 검색·google)은 20기기 중 17 완주. 홈 계산기 랜딩이면 완주는 된다.
- 글 안 링크 위치: X-CAFE-CALC B군은 글 끝 한 줄(c05 끝 안내, 11/22 tigerdj·divoone). 링크가 맨 끝이라 누르는 사람 수 자체가 8기기(23일)뿐 — 클릭 전 이탈인지는 카페 쪽 클릭 기록이 없어 확인 안 함.
- 결론: /dividend·/health-insurance에 계산 이벤트가 없어 '카페 유입이 계산을 안 한다'는 판단 근거 없음. 사이트 손대기(10/6 개발 중단)라 이벤트 추가는 결정 필요로만 올림. X-CAFE-CALC 12/4 판정 지표(calc 기기)는 /dividend에서 0으로만 나올 수 있다 → 지표를 'utm cafe 세션'만으로 보거나 이벤트 추가가 먼저.
