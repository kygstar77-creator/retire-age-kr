# 화면 부품 목록 (RULES 6-3)
| 부품 | 파일 | 참고한 경쟁 영상 | 처음 쓴 편 | 그 편 성과 |
|---|---|---|---|---|
| 지수 타일·선 차트·손그림 동그라미 | video/src/Weekly.tsx | 수페TV·WSJ·이코노미스트(longform-research.md) | 시안 v2 | — |
| 동네 지도 줌·보행 경로·거래 점 그래프·평당가 막대 | video/src/Tour.tsx | 인플레하우스·거부킴TV | 공덕동 시안 v3 | — |
| 진행 막대(왼쪽 5칸)·숫자 카운트업·자막 카드·장면 틀(Page)·로고 | video/src/parts/fm.tsx | 똑재TV 목록 복귀(study/2026-09-30) | A-1(미공개) | — |
| 검색창 질문 카드·흐름도·원문 인용 카드·도넛·숫자 쌍·쌓은 막대·두 선 그래프·음수 막대·원화 표·보유 상위 10·세금 카드+쪼개기 막대·기준선 막대·월별 기둥·계산기 입력+나이 기둥 | video/src/A1.tsx(A-1 전용, 다음 편에서 쓰면 parts/로 옮김) | 수페TV·똑재TV·은퇴머니 그림 종류(longform-research.md) | A-1(미공개) | — |
| 선+고점→저점 음영(여는 장면)·같은 출발점 100 선·낙폭 막대+6~8월 달력 띠·작은 막대 3폭(1년 전 테두리)·이익률 선 3개·쌍 막대(이익 배수 vs 주가 배수)·Form 4 카운터+표·원문 카드→가격 변동 범위 띠·일정 카드·입력 카드+나이 막대(0축)·정리 표·문장 카드(목록에 없는 장) | video/src/E1.tsx(E-1 전용, 재료 ep/E-1/e1props.py → video/e1.json, 단계 시점은 문장 속 말로 찾음) | 경쟁 3편 ytbreak(ep/E-1/compare.md) | E-1(미공개) | — |
| 세로 막대 계열(강조·테두리·점선 추정 막대+오차 막대)·범위 띠+실제 점·전후 가로 막대(배수 꼬리표)·도넛·저울·한글 공시 원문 카드·계단 막대 | video/src/parts/charts.tsx(범용 — 숫자는 전부 props) · E1.tsx의 mu8·guide·seg·dsdx·stairs·quotes2·scale·outlook 장면이 씀 | 경쟁 3편 ytbreak(ep/E-1/compare.md) — 전망치 대신 공시 원문을 그리는 그림 | E-1(10/3 예정) | — |
| 조건 꼬리표(CondTag)·흐름도(상자+꺾은 화살표, Flow)·칸 채우는 계산식(Tokens, 빈칸 점선→채움+아래 이름)·절벽 막대(CliffBars, 하한 점선+점프 괄호 꼬리표)·달력 줄(MonthRows, 해마다 12칸+구간 칠하기)·기간 띠(PeriodBand, n개월 눈금)·단계 카드(StepCards)·체크리스트(CheckList) | video/src/parts/explain.tsx(범용 — 글·숫자 전부 props, 색은 fm.tsx 토큰만) · D1.tsx(재료 ep/D-1/d1props.py → video/d1.json, 장면 16종) | 제도 설명형(건보료) — 계산식·조문·시점을 그림으로 | D-1(무음 리허설 10/1) | — |

## beats.tsx (2026-10-02 motion) — 영상미 고칠 점 5개, 새 편부터 opt-in
- `HookNumber {to, digits, prefix, suffix, label, color, dark, x, y, size}` — 여는 장면 첫 1.2초 안 숫자. 마지막 값 = 사실표 값.
- `beatCues(cues, total, fps, maxGap=6)` + `<Beat cues n>{(focus, o) => ...}</Beat>` — 문장 시작 프레임(at(s,i))을 넣으면 6초 넘는 빈틈에 스스로 다음 요소로 초점을 옮긴다. `o(i)`를 각 요소 opacity로.
- `<Drift frames seed>` — 오래 머무는 표·원문 판을 장면 길이 동안 1.035배까지 천천히 민다.
- `HeroNumber {to, top, bottom, source, start}` — 화면 가득 숫자 하나. 한 편 2번까지, 여는 장면에 안 씀.
- `PenMark {kind: under|arrow|bracket, x, y, w, h, cue, seed}` — 펜 긋는 숫자는 글자색 잉크.
- `<Wipe seed dur at>` — 장면 맨 앞에 넣는다. 방향·띠 색이 seed(편 이름)로 바뀐다.
- 미리보기: Root.tsx `MotionKit` 컴포지션(12초), 렌더 ep/E-1/motion_preview/motionkit_5fix.mp4.
- 관문: `py -3.12 work/video/motioncheck.py <렌더 mp4>` — 첫 3초 움직임·정지 15초 이하. 경쟁 수치는 motion-bench.md.

## parts/ledger.tsx (2026-10-02 23:07, PD · E-2 테슬라에서 처음)
- ComboBarLine(10분기 매출 막대+이익률 선, 최고·최저 꼬리표) · Waterfall(총이익→비용→영업이익) · SlopeRows(전→후 기울기 줄, 값 글자 46px 벌림) · AreaCircles(넓이 비교 원 2개) · FillBar(계획 테두리 안 실적 채움+남은 칸+비교 막대). 다른 종목 장부 편에 그대로 쓴다.

## parts/rank.tsx (2026-10-03 02:31, PD · N-1 나 vs 남들에서 처음)
- PctStrip(100칸 띠 + 역삼각 자리 표시, 왼쪽=상위) · HundredBars(100칸 막대, cap 넘는 칸 ≈ 표시) · PctRuler(P10~P90 눈금자, 값 두 줄, 핀) · DivergeRows(0 기준 좌우 증감 막대, 음수 파랑 왼쪽). 나 vs 남들 다음 편에 그대로 쓴다.

## parts/receipt.tsx (2026-10-03 10:32, PD · R-1 1억의 1년 영수증에서 처음)
- ReceiptPaper(영수증 종이: 위에서 내려오며 줄마다 인쇄, 세금 빨강·통장 굵은 주황·빈 줄 빗금) · Stamp('확인 안 함' 비스듬 도장) · DotStrip(상품 하나 = 점 하나 띠, 중앙·최저·최고) · Coins(분배금 동전 n개 떨어짐). X-SERIES-1 영수증 다음 편에 그대로 쓴다.

## parts/reverse.tsx (2026-10-06 02:44, PD · M-1 월배당 거꾸로에서 처음)
- RuleCards(규칙 카드 줄, 안 나온 카드는 점선 자리표) · Gauge(가로 문턱 게이지: 문턱선·차오름·목표 꼬리표) · Timeline(구간 띠 3칸) · FlowBoxes(거꾸로 화살표 상자) · ProductCard(상품 카드 + 분배율·필요한 돈) · Calendar12(12칸 달력·동전) · GroupBars(묶음 막대, 나란히 — 쌓지 않음) · Grid(표·칸 도장·강조 칸). 쓰임 video/src/M1.tsx, 재료 ep/M-1/m1props.py
- 2026-10-06 02:44 PD · 공용 고침: motion/TallyBars 꼬리표 모드에서 valueText ''면 꼬리표 안 그림(빈 검은 점 생김) · motion/TallyFrame 자막([자막]) 길면 줄바꿈(nowrap이라 판 밖으로 넘쳤음)
