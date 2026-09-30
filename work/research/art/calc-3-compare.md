# calc-3 뻔함 관문(21번) 비교 — 퇴직금·실업급여 → '몇 살에 은퇴' 연결 (firemap-artist, 2026-10-01 08:47)

직접 받은 것만 적는다(curl 모바일 UA로 정적 HTML·JS 청크를 받음, 계산 버튼을 눌러 결과 화면을 본 것은 아님). 못 본 것은 '확인 안 함'.

| 경쟁 | 결과 뒤 은퇴·노후 연결 | 숫자 넘김 | 근거 |
|---|---|---|---|
| **MyMoneySim** mymoneysim.com/severance · /unemployment | **있다.** 퇴직금: 카드 "퇴직금까지 더하면 노후는? 지금 자산에 퇴직금을 더해 은퇴 시점을 다시 계산해 보세요 · 파이어족 시뮬 →". 실업급여: "쉬는 동안 노후 준비도 점검 · 지금 자산으로 몇 살에 은퇴할 수 있는지 확인하세요 · 파이어족 시뮬 →". /fire 제목 "파이어족 은퇴 계산기 — 노후자금·은퇴 나이 확률로" | **안 넘김** — 페이지 JS 청크에서 `href:"/fire"` 고정 링크(쿼리 없음). 다음 계산 카드 3개(연봉·IRP·파이어) 중 하나 | curl 08:46 HTML·`_next/static/chunks/app/severance/page-2b174a…js` |
| 국민연금 중앙노후준비지원센터 csa.nps.or.kr | 퇴직금 추정 뒤 '간단재무설계·예상연금조회' 링크 | 안 넘김(따로 다시 입력) | calc-competition/severance.md(9/30 열어 봄) |
| 사람인 m.saramin.co.kr/helper-tool/retire · /unemp | 정적 HTML에 '은퇴·노후·연금·IRP·재무설계' 0건 | — | curl 08:45 |
| 인크루트 lab.incruit.com/editor/unemp · /retire | 같음 0건 | — | curl 08:45 |
| 고용노동부 moel.go.kr/retirementpayCal.do · 고용24 모의계산 | 같음 0건 | — | curl 08:45 |
| CalcTools calctools.co.kr/finance/severance-pay · unemployment-benefit | 같은 사이트에 은퇴자금·퇴직연금 계산기가 있으나 이 두 페이지 HTML에 그쪽 링크 0건 | — | curl 08:46 |
| 네이버 임금계산기 위젯 · 잡코리아 | 확인 안 함(네이버 위젯은 브라우저 막힘, 잡코리아 도구 주소 404) | | |

## 3줄
- 경쟁이 잘하는 것: 공식 기관은 정확·조문, 취업 포털은 입력 편의, **MyMoneySim은 우리와 똑같은 '퇴직금·실업급여 → 몇 살에 은퇴' 다음 카드를 이미 걸어 놨다.**
- 우리가 따라갈 것: 결과 바로 아래 한 번 누르면 은퇴 계산으로 넘어가는 연결(이미 있음 — SeveranceCalc·UnemploymentCalc가 금액을 financialAsset에 더해 넘김).
- 우리가 다르게 할 것: 버튼 '문구'는 경쟁과 같아 보인다. 다른 점은 숫자를 넘긴다는 것인데 **누르기 전엔 안 보인다.** → 누르기 전 결과 카드에 '이 돈이 은퇴 나이를 몇 개월 당기는지'를 숫자로 보여 줘야 첫 3초에 달라 보인다.
