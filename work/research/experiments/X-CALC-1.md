# X-CALC-1 · 계산기 결과 다음 단계 (firemap-product-dev, 근거 파일 10/2 · 장부 experiments-registry.md 32행)
비교: A "이 돈이면 몇 살에 은퇴?"(주황 버튼, 결과 카드 바로 아래) vs B "공유 카드 먼저"(artist 제안 은퇴 영수증 카드, 10/15 visual-designer·product-dev).

## ① 근거 데이터 (firemap_events, 9/2~10/2 30일, internal·bot 표시 뺀 값, 10/2 17:5x 조회)
| 항목 | 값 |
|---|---|
| 계산기 3종 화면(screen_view severance·unemployment·salary) | 215회 · 80기기(9/30부터). 10/1 이전 몰림 봇(channels.md 5번)은 bot 표시가 없어 섞여 있음 — 사람 수는 확인 안 함 |
| 결과→은퇴 클릭(*_to_fire) | severance_to_fire 2기기 · unemployment·salary 0 |
| 다음 계산기(next_calc_click) · 쿠팡(coupang_click) · 입력 시작(calc_input_start) | 외부 0 |
| 계산기 방문 전에 파이어 결과 화면을 본 기기(저장 입력 있음 추정) | 1/80 = 1.3% |
| 사이트 전체 share 이벤트 | 83회 · 39기기(계산기 화면 공유는 아님) |
| 'N년 앞당겨져요' 숫자 줄 조건 충족 비율(입력 격자 180개 균등 가정, design/calc-3/build/gainrate.mjs) | 저장 입력 있는 사람 중 실업급여 41.1% · 퇴직금 30.0% → 전체 방문자 기준 약 0.5%(1.3%×41%) |

## ② 분석
- A의 클릭은 30일 2건이라 지금은 A·B를 비교할 표본이 없다. 분모(사람이 넣은 입력)가 0이라 비율을 낼 수 없음.
- 숫자 줄은 저장 입력이 있어야 뜨는데 계산기 방문자 대부분이 처음 온 사람(98.7%) → A의 '누르기 전 답'은 거의 보이지 않는다. 기획 기준 10% 미만 → 후보 ③(생활비 N개월치, 같은 .fm-gain 자리) 교체 판정 요청을 올렸다(today.md 10/2).
- B(공유 카드)는 사이트 전체에서 share 39기기가 있어 공유 행동 자체는 있다. 계산기 결과 공유는 아직 없음(부품 없음).

## ③ 예측 (틀리면 접는다)
- A: 외부 calc_result 30건 쌓인 시점에 *_to_fire / calc_result ≥ 10%.
- B: 공유 카드 공개 후 2주, 계산기 결과 공유 / calc_result ≥ 5%, 공유로 들어온 새 기기 ≥ 5.
- 둘 다 미달이면 다음 단계 칸은 버튼 1개(A)만 남기고 B 부품은 지운다.

## ④ 판정일·접는 기준
- 판정 10/28(장부). 그때 외부 calc_result가 30건 미만이면 '표본 부족'으로 기록하고 판정 대신 유입(검색·카페 링크) 쪽 원인 한 줄 — 화면을 더 바꾸지 않는다.
- 측정: calc_result·*_to_fire{gain_shown}·*_gain_view{gain_years}(10/2 dev 추가) · B는 utm_source=share.
