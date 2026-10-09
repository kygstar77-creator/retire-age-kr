# G-1 모션 설계 (firemap-motion-designer)

## 장면마다 무엇이 움직이나 (script.md 장 기준 · PD G1.tsx 28장면 위에서)
| 장 | PD 장면 kind | 움직이는 것 | 부품 | 우선 |
|---|---|---|---|---|
| 0. 여는 장면 첫 3문장 | twin(영수증 두 장) | 어두운 hook 판 '지금 663만원' → 1월 고점 점으로 빨려 듦 → KRX 1년 선 그려짐 → 산 날 점에서 1천만원 덩이가 막대 자리로 날아가 오늘 값만큼 줄어듦(줄어든 몫 빗금, 낸 돈 점선) → 1년 전 같은 규칙 → 선 흐려지고 '같은 금, 산 날만 달랐다' | **BuyDateOpen(새, 10/9 통과)** | 1 |
| 0. 넷째 문장~ | cards·road | 카드 순환(PD 그대로) | — | — |
| 2. 영수증 4장 | line·loss | 선 위 점 4개가 차례로 찍히고 막대 4개 줄어듦 — BuyDateOpen과 같은 문법(점→막대)을 4개로 이어 받으면 장면 사이 끊김 없음 | BuyDateOpen 확장(buys 4개, 다음 회차) | 2 |
| 3. 세 조각 | formula·pieces | 폭포 막대: 달러 금값 +6.65% → 환율 −3.38% → 웃돈 −7.26% 차례로 쌓이며 끝 막대 = −4.43%(곱 검산) | **WaterfallPieces(새, 2026-10-09 통과)** | 2 |
| 4. 산 길 4개 | cards·law·split | 골드바: 1천만원 막대에서 부가세 909,091원 조각이 떨어져 나가 출발선이 뒤로 | split(PD) + 떨어짐 | 3 |
| 6. 산 값까지 | asym | 계단: 179,000 → 269,810원, −33.66%로 내려온 거리 vs +50.7% 올라갈 거리를 같은 축에 나란히 | 새 부품 후보 `AsymClimb` | 2 |
| 5·7 | line·quote·count·stamps·law·end | PD 그대로(원인 단정 금지 장 — 과한 움직임 넣지 않음) | — | — |

## 첫 장면 BuyDateOpen (2026-10-09)
- 부품 work/video/src/motion/BuyDateOpen.tsx · props motion_preview/g1open.py → g1_open.json · 미리보기 motion_preview/g1_open.mp4(960×540, 12.2초 어림 — 음절÷5.65)
- 정직성: 산 날 점 = 그날 실제 종가(솎기에서 산 날 보존, assert) · 막대 높이 = 오늘 값÷낸 돈 비례, 0 기준선 공유 · 점선은 '낸 돈' 한 뜻만 · 숫자 굴리지 않음 · hook 숫자는 man(calc)에서 만들어 공개 전날 calc 재실행을 따라감
- motioncheck: 움직임 73% · 첫 움직임 1.0초 · 최장 정지 1.5초
- 심사 review_open.md(평균 7.67) · 묶음 board_open.png · 날아가는 구간 fly_check.png
- 실사 AI 장면 없음 → containsSyntheticMedia 해당 없음

## 3장 세 조각 WaterfallPieces (2026-10-09)
- 부품 work/video/src/motion/WaterfallPieces.tsx · props motion_preview/wfprops.py → g1_wf.json · 미리보기 motion_preview/g1_wf.mp4(34.5초 어림)
- 말 구간: '3.' 장 '작년 영수증부터' ~ 장 끝(PD piece1·prem·piece1b 세 장면 자리를 한 장면으로)
- 정직성: 글자 = 곱 %(calc_out), 막대 = 로그 몫 %p(합 = −4.43%, 값 아래 '막대 ±x.x%p'로 밝힘), 0선 = 산 날 값 · 빨강 오름·파랑 내림·주황 합계
- motioncheck 최장 정지 2.5초 · 심사 review_wf.md 9·6·6 평균 7.0 · 묶음 board_wf.png · 실사 AI 장면 없음

## [요청] firemap-video-producer — G-1 녹음 뒤
1. 녹음 뒤 `py -3.12 work/research/longform/ep/G-1/motion_preview/g1open.py`(voice.json 길이 자동) → G1.tsx open 장면(지금 kind 'twin')을 `<BuyDateOpen {...open} />`(TallyFrame 자식)로 바꾸고 scene.frames는 g1_open.json 값. 단 open은 '0.' 장 첫 3문장만 — 넷째 문장부터는 PD 장면 그대로.
2. 렌더 뒤 첫 장면만 `--frames=0-<끝> --scale=0.5`로 motioncheck(최장 정지 3초 이하) · 3.5초·6.5초쯤 덩이가 점에서 출발·판 안인지 한 번 보기(M-1 때 실제 녹음에서 정지가 새로 생겼음).
3. 화면 글자 늘어남: hookTop·hookBig·sameText(전부 대본 원문 조각) · '점선 = 낸 돈 1천만원' · 'YY.MM.DD 산 날' → lfrender text 뒤 편집 재서명.
