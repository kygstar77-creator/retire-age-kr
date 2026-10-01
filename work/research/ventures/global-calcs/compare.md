# 나라별 계산기 한 사이트 — 경쟁 실측 (compare.md)

- 요청: today.md [기획 요청·조사 요청] 나라별 법에 맞는 계산기(순돌이 17:04, 사장님 아이디어). ① 경쟁 = 이 파일, ② 수요 = demand.md, ③ 공식 원문 = sources.md.
- 조사: firemap-venture-research-global, 2026-10-01 17:06~17:22 KST. 로그인 없음. 트래픽은 Similarweb 공개 쪽(2026년 8월 데이터) — WebFetch 요약 라벨이 "Total Visits Last 3 Months"라 **월/3개월 합 확정 못 함**, 받은 값 그대로. 교차 1건: HypeStat salaryaftertax.com 월 209,131(날짜 표기 없음).

## ① 상위 5

| 순위 | 사이트 | 나라 수(직접 셈) | 세법 연도·갱신 | 수익 | Similarweb(26-08) | 나라 고르기 |
|---|---|---|---|---|---|---|
| 1 | talent.com/tax-calculator | **65+**(ISO 70개 서브도메인 하나씩 열어 셈, ca 403·범위 밖 확인 안 함) | 제목 "2026"만, 영국도 2026/27 아님, Last updated 없음 | 애드센스+검색광고, 본업 구인 | 9.3M, 세계 7,118위(**도메인 전체**) | 서브도메인 `kr.talent.com/en/tax-calculator` |
| 2 | numbeo.com/salary-calculator | **107**(select 옵션 수) | 연도·갱신일 표시 없음 | 애드센스+Premium·API | 2.1M, 25,776위(도메인 전체, 주력 생활비) | 쿼리 `?country=` |
| 3 | salaryaftertax.com | **19** | 쪽마다 "updated: 월 연도"(독 2026-09, 호 2026-07, 일 2026-05), 국세청 링크 | PubNation(Mediavine 계열) 광고 + **이사 견적 리드** + 뉴스레터 | 487.5K, 116,890위 · 유입 74.37% 검색 · 캐나다 19%·아일랜드 13%·독일 8% | `/de/salary-calculator`, `/salary-calculator/uk` 혼재 |
| 4 | worldsalaries.com | 세금 **12**(+미국 주별) | "Tax year 2026", 영 2026/27, 2021~2026 선택 | Raptive 광고 | 93.9K, 419,862위, 전월 −25.99%, 체류 24초 | `/germany-tax-calculator`, **금액별 쪽 대량**(`/50000-after-tax`) |
| 5 | icalculator.com | **207**(2025-09-04 아카이브 기준) | 아카이브 "2025 tax tables" · **측정 중 사이트 다운**(Cloudflare 522/525 ×4) | 애드센스 | 83.1K, 437,443위, 전월 −8.01% | `/japan.html` 180 + 나라 서브도메인 27 |

뺀 곳: calculator.net(42M, 세후 계산은 **미국만**) · omnicalculator(9.1M, 나라 세금은 영·호·파키스탄·필리핀 몇 개) · countrytaxcalc.com("111+ countries", Raptive, 521,939위, 나라 수 직접 안 셈) · take-home-pay.com("Tax Year 2025" 남음, 트래픽 확인 안 함) · salaryaftertax.org(접속 불가) · paychecktaxcalculator.net(403).

## 다섯 곳 공통 빈틈 (실측)
1. **여러 나라 은퇴·연금 계산기를 가진 곳 0/5** — 연금은 월급 공제 한 줄로만 나온다. (파이어맵 본업과 맞닿는 칸)
2. 쪽마다 갱신일을 적는 곳 1/5(salaryaftertax.com). 나머지는 연도만이거나 없음 → '원문 대조 도장'이 보이는 차이가 될 수 있다.
3. 나라 수 많은 곳은 얕다: talent.com 영국 = 소득세·NI 2개만(연금·학자금 없음), icalculator는 다운, numbeo는 연도 표시 없음.
4. 한국은 talent.com(5개 공제 분리)만 있고 salaryaftertax·worldsalaries엔 없음.

## 세 줄
- **경쟁이 잘하는 것:** 나라 수(65~207), 도메인 힘(talent.com 9.3M), 금액별 롱테일 쪽 대량(worldsalaries), 갱신일·국세청 링크(salaryaftertax).
- **따라갈 것:** 쪽마다 세법 해·갱신일·공식 원문 링크, 나라별 고정 주소, 금액별 결과 쪽은 품질 기준 통과분만.
- **다르게 할 것(예술가 판정 전 후보):** 은퇴·연금까지 이어 보기(0/5), 원문 대조 도장(1/5만 갱신 표기), 나라 수 대신 깊이(첫 판은 원문·대조 계산기가 다 있는 영국·호주·독일·네덜란드 같은 '쉬움' 나라만 — sources.md).

## 숫자로 본 함의(판정은 본부장)
- 돈: 검색량 1위 독일어권은 CPC $0.02(ET) → 광고로는 약함. 미국 $1.82~3.35·호주 $2.68·영국 $0.82~1.81·일본 $1.34(demand.md). salaryaftertax.com은 광고 외에 **이사 견적 리드**로 번다.
- 상한 참고: 19개국·전문 사이트 1위권(salaryaftertax.com)이 Similarweb 487.5K(월/3개월 미확정)·HypeStat 월 209K. 이 칸 순수 계산기 사이트의 실측 천장이 그 정도다.
- 미국은 수요·CPC 최대지만 주세 50곳+로 AI 단독 유지 '어려움'(sources.md).
