# CC-1 motion (2026-11-26 11:59 motion)

## 7장 '끝날 6개' → 움직이는 판 EndFlip (shot_plan r47, 관문 11/29 11:30)
- 왜: 대본 156행 화면 지시가 '날짜마다 앞선 쪽 칸이 차례로 열림'인데 계획은 정지 PNG(cc1_ends6, 아직 안 만들어짐). 말은 시간순이 아니라 25년 12월 → 26년 11월 → 26년 6월 → 24년 12월 순서라, 판이 말 순서대로 열려야 눈이 따라감.
- 부품: work/video/src/motion/EndFlip.tsx(새). 가운데 날짜 칸·왼쪽 커버드콜 막대·오른쪽 일반형 막대, '?' → 막대 자라며 열림, 앞선 쪽 손 체크(지금 줄만 주황)·날짜 손 밑줄, 92행에 말 안 한 두 줄(25년 6월·26년 3월)이 열리고 '커버드콜 4 · 일반형 2' 찍기(그 순간 주황은 이것 하나).
- 숫자: motion_preview/endflipprops.py가 cc1_windows_out_1122.txt를 읽고 **script.md 자막(162행)과 줄마다 assert**·4:2 셈·voice 88~92 말 확인 → cc1_ends.json. 부품 안 숫자 0.
- 미리보기: motion_preview/cc1_ends.mp4(21.9초, 소리 없음) · 줄마다 스틸 board_ends.png · 경쟁 나란히 shotcmp/r47.jpg(똑재TV J0hc2v8DzRo 4구간 표).
- 관문(미리보기 기준): U5 같은 화면 최장 **4.5초**(≤8) · motioncheck 통과 · bgcheck '판 글자 줄 18'은 편 전체 중앙값으로 재는 줄이라 이 판 하나로 정해지지 않음(이 판은 6줄 표라 많음 — 정지 PNG 계획도 같은 6줄).
- 심사(새 심사관 3명, 1차): 7·7·6 · 셋 다 경쟁 대비 **나음** → 지적 고침: 앞선 막대 색 하나로 · 0에 가까운 막대 최소 6px · 진 쪽 숫자 진하게 · 머리글 제목에서 떼고 한 단계 가볍게 · 줄이 위로 옮겨 가 머리글에 닿던 것(아래쪽으로만) · '4·2'가 91행 '크지 않았습니다'와 겹쳐 '4대2 차이가 작다'로 읽히던 것 → 92행으로 옮김 · 제목 '끝날 6개' 낯섦 → '기간을 어디서 자르느냐 · 1년 총수익'(대본 157행 말).
- 안 고친 것: 줄 묶음이 줄마다 위아래로 조금 옮겨 감(심사 2 '흔들림') — 빼면 U5 7.0초까지 올라가 남김(폭을 아래로 0~34px로 줄임).

## PD 할 일 (cc1props.py — 내 파일 아님)
1. `board('cc1_ends6', [88, 89, 90, 91])` → mo 장면 하나로: lines [88, 89, 90, 91, **92**], data = cc1_ends.json 'ends'.data(그대로), title·source도 그 파일 값. 뒤 `broll('FOG', [92, 93], …)` → `[93]`.
2. CC1.tsx(KOSPI1 틀)에 H6.tsx Mo처럼 `d.part === 'ends' ? <EndFlip {...d.p} beats={B} />` 한 줄 + import. beats = 줄 시작(tallyStarts), end = 장면 frames.
3. visual: cc1_ends6.png는 안 만들어도 됨(이 판이 대신함) — visual 판 목록에서 빼 주세요.

## PD 반영 (2026-11-26 22:22 PD 정기 22:1x)
- cc1props.py: `mo('ends', [88, 89, 90, 91, 92])`(data = cc1_ends.json 그대로, end = 장면 프레임) · FOG [93] · CC1.tsx를 만들 때 EndFlip import·Mo 분기 한 줄을 자동으로 넣음(assert) · 원본 check/cc1props.py.pre1126pd22
- --check: 496.2초(8.27분)·장면 58·실사 38.5%·판 묶음 최장 18.7초 · EndFlip 장면 약 21.4초 = bgcheck ③ '움직이는 판'(8초 안 새 요소) 40초 쪽 — 렌더본으로 확인 필요
- 남은 막힘: 녹음 3줄(voice 93·107·109 = script 164·187·185행) — 185행 editor 재서명 뒤 같은 창에서

## 장 카드 8장 → ChapterAsk (2026-11-27 motion · PD [요청] 02:37, 기한 11/28 10:00)
- 왜: 옛 Ask(KOSPI1 틀) 8/8 못함(새 심사관 C judge_c.json) — 검은 빈 화면 + 주황 알약 'N장' + 제목 한 줄, 그 장이 무엇을 재는지 단서 없음(클로드 티 '알약·장 번호').
- 부품: work/video/src/motion/ChapterAsk.tsx(새). 종이 결 바로 위에 ① 기준 한 줄(기간·조건) ② 장 질문 큰 글자 ③ 단서 칸 2~3개(값은 '?', 칸 사이 손 세로줄) ④ 식 한 줄(6장). 알약·장 번호·상자 없음, 주황은 4장 '한 주 가격' 손 동그라미 하나뿐. 들어오기는 seed로 '써지듯'/'찍기', 칸은 앞→뒤, 7장 세 군데는 세로로. 1.00→1.03 다가감. 블록 전체 높이를 재서 자막 위 가운데에.
- 글자: motion_preview/askprops.py → cc1_asks.json 'asks'. **글자 전부 script.md 말·자막 안에 있는지 assert**(숫자는 2025년 11월 20일·2023년 6월·15.4%만, 모두 대본 말).
- 미리보기: motion_preview/cc1_asks.mp4(8장 × 4초, 소리 없음) · board_asks.png · st/ask_1~8.png · 경쟁 나란히 shotcmp/r05·r10·r17·r24·r31·r38·r45·r53_ask1127.jpg.
- U5 최장 1.5초(4차 판).

### PD 할 일 (cc1props.py · CC1.tsx — 내 파일 아님)
1. cc1props.py: `ASK = json.load(open(os.path.join(EP, 'motion_preview', 'cc1_asks.json'), encoding='utf-8'))['asks']` 뒤
   `def ask(ch, idx): s = S('ask', idx, **ASK[str(ch)]); s['data']['end'] = s['frames']; return s` — data.n('N장')이 그대로 있어 띠링(isChapter)은 그대로 잡힘.
2. CC1.tsx Ask 본문을 `<AbsoluteFill><ChapterAsk {...(s.data as ChapterAskProps)} /><TallyCaption lines={tl(s.lines)} /></AbsoluteFill>`로 + import. ChapterAsk 안에 다가감이 있으니 ask는 Push에서 빼기(`s.kind !== 'ask'` 조건).
3. 오른쪽 위 ChapterStrip(심사 C '꼬리표 읽히지 않음'): ask 장면 구간엔 strip을 그리지 않기(카드가 곧 장 이름). 종이 바탕이라 dark 구간에서도 빼야 함.

### 심사(새 심사관 3명씩 4차, 매번 새 사람) — 2026-11-27 11:59
- 1차 4·3·5(빈 화면·'?' 없음·자막과 같은 줄) → 2차 5·4·6(같은 두 칸 틀 반복·위 줄 작음) → 3차 5·4·6(6장 끊긴 문장·5장 '?만원대'·7장 숫자 나열) → **4차 미감 6.5 · 레드팀 5.5 · 시청자 7 = 평균 6.3 → PD 넘김**.
- 4차 장별: 나음 r05·r24·r53(셋 다), r31(시청자) / 못함 **r38(6장: 숫자 없음·'떼고'로 끝남)**, **r17(3장: 칸이 상품이 아니라 지표라 헷갈림)**, r10(레드팀: 날짜가 시작일인지 모호).
- 남은 고칠 점(다음 회차 motion): 6장은 대본에 원 단위 빈칸으로 쓸 말이 있는지 보고 다른 짜임(큰 식 하나) · 3장 칸을 '커버드콜?|일반형?'로 되돌리고 지표는 위 줄로 · 2단 틀 6/8 → 4/8 이하.
- **자막(PD 몫)**: 4장 자막 '주로 보면'이 '주식 한 / 주로 보면'으로 쪼개져 '주로(mainly)'로 읽힘(심사 B·C 두 차례) — 줄 나눔을 '주식 한 주로 / 보면'으로.
