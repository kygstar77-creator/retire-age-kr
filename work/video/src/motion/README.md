# video/src/motion — 재사용 모션 부품 (firemap-motion-designer)

숫자는 props로만 받는다(spec·facts.txt 원문). 부품 안에 숫자를 쓰지 않는다. 편마다 `seed`(편 이름)를 바꿔 방향·간격·좌우가 달라진다 — 같은 틀 반복은 유튜브 '진정성 없는 콘텐츠' 신호.

| 부품 | 하는 일 | 근거 |
|---|---|---|
| `RollNumber` | 숫자 자리마다 **제 숫자만** 아래(또는 위)에서 올라와 임계 감쇠로 선다. 0프레임에도 숫자 70%가 보인다. 가짜 중간 숫자 없음 | 모션 475 'BUILD THE FLOOR' |
| `settle(frame,fps,stiffness)` | 튀지 않는 스프링(damping=2√k) | 같음 |
| `CardToBar` | 숫자 밑 바닥 선 → 차트 0 기준선, 숫자 → 제 막대 이름표, 비교 막대가 옆에 자람. 막대는 기준선에서만 자란다, 높이는 값 비례 | 모션 475 'Taxtello' 물체 전환 + dataviz |
| `ZoomOutOpen` | 롱폼 첫 장면(1920x1080, TallyFrame 안). 점 하나 확대 → 줌아웃하며 갈래 N개 '?' → 날짜 축·같은 금액이 갈래를 따라감 → 갈래 빠지고 간격 막대(세금 전→뒤, 값 비례). 갈래는 대본 순서 고정(순위 암시 금지) | 모션 475 #5 · R-1 10/5 |
| `ShortIntro` | 위 둘을 묶은 쇼츠 첫 2초(1080x1920). Root id `ShortIntro` | — |

## 쇼츠에 붙이는 법
1. props JSON을 만든다(예 `video/intro_e2_interest.json`): seed·chip·title(spec 제목 그대로)·hook·a·b·unit·source·numW(큰 숫자 폭 px, 스틸로 잼)·aFirst(카드 순서와 맞출 때).
2. `npx remotion render src/index.ts ShortIntro <out>.mp4 --props=<json> --codec=h264 --pixel-format=yuv420p`
3. 쇼츠 spec에 `"intro_mp4": "<절대경로>"` → `py -3.12 work/cardshort.py <spec> <out>`. 인트로가 있으면 표지(cover/cover_png) 대신 들어가고, 카드는 다 자란 상태(t=2)로 시작한다.
4. `py -3.12 work/video/motioncheck.py <out>`(정지 ≤15초) · 0초·0.5초·2.0초·2.1초 프레임에 사실표 밖 숫자 0 확인 · 심사 3명 평균 7.

## 편마다 바꿀 것(반복 방지 체크)
- seed 바꾸기(자동), 막대 좌우(aFirst), 비교 상대(값 2개가 아닌 경우 다른 부품), 강조색은 spec 카드 색 안에서.
- 매 편 '숫자→막대'만 쓰지 않는다: 다음 후보는 줌아웃(모션 475 #5), 계산 곡선(#3).

## 롱폼 첫 장면 줌아웃(ZoomOutOpen) 쓰는 법
1. 재료 JSON: `seed·dot·names·nameAt·from·to·q·travel·gap·gapHead·pre[글자,값]·post[글자,값]·cut`. q·travel·gap = 말 2·3·4 시작 프레임. 예: `research/longform/ep/R-1/motion_preview/zoomprops.py`가 r1.json·facts.txt 대조로 만든다.
2. 미리보기(본편 Root와 따로): `npx remotion render src/motion/preview/entry.ts OpenZoom <out>.mp4 --props=<json> --codec=h264 --pixel-format=yuv420p`
3. 본편: 장면 컴포넌트에서 `<ZoomOutOpen {...zoom} />` (TallyFrame 자식으로).
4. 편마다 바뀜: seed로 점 높이·부채 폭. 갈래 순서는 바꾸지 않는다(순위처럼 읽힘). 비교할 값이 둘이 아니면 막대 단계는 다른 부품으로.

## 롱폼 첫 장면 거꾸로 묻기(ReverseAsk) 쓰는 법 — '목표에서 거꾸로' 주제(월배당·은퇴 자금)
1. 재료 JSON: `seed·big·ask0·goal·goalSub·bars[[이름,값,글자]]·low{i,v,label,times,tag}·also[{i,v,label,times}]·note[[i,글자]]·fwd·nope·rev·land·grow·hi[[프레임,번호]]·low0`. 예: `research/longform/ep/M-1/motion_preview/m1props.py`(calc_out.txt·대본 assert 대조).
2. 미리보기: `npx remotion render src/motion/preview/entry.ts M1Open <out>.mp4 --props=<json> --scale=0.5 --pixel-format=yuv420p`
3. 규칙: 한 막대를 다른 기준으로 늘리면 같은 기준이 있는 막대는 모두 `also`로 같이 늘린다(없으면 `note`로 이유). 말이 가리키는 막대=진한 잉크, 주황=핵심 숫자(low)만.
4. 편마다 바뀜: seed로 막대 폭·간격·화살표 휨·격자 간격. 막대 순서·높이는 바꾸지 않는다.

## 롱폼 첫 장면 산 날 영수증(BuyDateOpen) 쓰는 법 — '언제 샀나' 주제(금값·주가 고점 매수)
1. 재료 JSON: `seed·hookTop·hookBig·hookOut·pts·min·max·ticks·xlabels·draw·now[값,글자]·paid·paidText·buys[{i,v,date,value,text,pct,at}]·same·sameText`. 예: `research/longform/ep/G-1/motion_preview/g1open.py`.
2. 미리보기: `npx remotion render src/motion/preview/entry.ts G1Open <out>.mp4 --props=<json> --scale=0.5 --pixel-format=yuv420p`
3. 규칙: 선을 솎을 때 산 날은 반드시 남긴다(점 = 그날 실제 값) · 점선은 '낸 돈' 한 뜻만 · 막대 높이 = 값÷낸 돈 · 덩이는 점에서 출발('center bottom' 축소면 top=py−h0).
4. 편마다 바뀜: seed로 막대 폭·간격. 산 날 순서는 대본 순서 그대로.

## 세 조각 폭포 막대(WaterfallPieces) 쓰는 법 — 곱으로 된 변화 분해(금값 = 달러 금값 × 환율 × 웃돈 등)
1. 재료 JSON: `seed·min·max·zeroText·steps[{name,sub,pp,text,at}]·total{…,won}·prem[[글자,프레임]]·hit·note[글자,프레임]·intro`. 예: `research/longform/ep/G-1/motion_preview/wfprops.py`(calc_out %p assert).
2. 미리보기: `npx remotion render src/motion/preview/entry.ts G1Waterfall <out>.mp4 --props=<json> --scale=0.5 --pixel-format=yuv420p`
3. 규칙: 막대 길이 = 로그 몫 %p(합이 정확히 전체), 글자 = 곱 % — 둘이 다르니 값 아래 '막대 %p'를 반드시 보인다(레드팀 2026-10-09) · 주황은 합계만 · 판 위 끝 254~300은 [자막] 띠 자리.
4. 정지 방지: 말마다 다가갔다 물러남(pulse), 사건 사이 6초 넘으면 가운데 한 번 더. 편마다 seed로 칸 폭·막대 폭.

## 내려온 폭 vs 올라갈 폭(AsymClimb) 쓰는 법 — '떨어진 만큼 올라서는 모자란다'(손실 회복 산수, 고점→오늘→고점)
1. 재료 JSON: `seed·top·now·peakText·nowText·peakName·nowName·downText·upText·downBase·upBase·intro·drop·slide·climb·base·short·shortText·shortLack·fee[글자,프레임]`. 예: `research/longform/ep/G-1/motion_preview/asymprops.py`(calc_out 첫 줄 assert, 문장 안 시점은 음절 비례).
2. 미리보기: `npx remotion render src/motion/preview/entry.ts G1Asym <out>.mp4 --props=<json> --scale=0.5 --pixel-format=yuv420p`
3. 규칙: 막대 높이 = 값(0부터) · 두 폭은 같은 높이라 '같은 폭' 글자만, 차액 숫자는 만들지 않는다 · 빗금 = '내려온 폭' 한 뜻(모자란 몫은 무늬 없는 주황 면) · '34%만 오르면' 상자는 속을 비워 아래 빨강이 비치게(레드팀 2026-10-10).
4. 정지 방지: 말이 가리키는 칸으로 옆 이동 + 사건마다 pulse + 끝 도장 뒤 두 % 글자 차례로 짚기. 편마다 seed로 막대 폭·칸 위치·고점 높이.

## 겹침·같은 화면 관문(OverlapProbe · ovcheck.mjs · lfrender screen) — U5 (10/11)
- 렌더 전: `py -3.12 work/lfrender.py overlap <ep폴더>` → 편 컴포지션 옆에 OverlapProbe를 붙여 1초마다 숫자 글자가 카드·글자·도형에 가려지는지 잰다(ep/<편>/overlap.json). `render`가 자동으로 부르고, 1건이라도 있으면 렌더하지 않는다.
- 렌더 뒤: `py -3.12 work/lfrender.py screen <ep폴더>` → 같은 화면 최장 8초 이하(그래픽 영역 4% 넘게 바뀌어야 새 화면) + 겹침 0 → out/<편>.screen.json. ytupload가 롱폼 렌더본(10/11 12:00 뒤)은 이 기록이 통과여야 올린다.
- 가림으로 치지 않는 것: 화면 절반 넘는 판(장면 층·훅 카드), 글자 뒤 바탕과 같은 색 가림막(차례로 드러내기), 선만 있는 도형(손그림 동그라미). 글자끼리는 실제 글자 자리로 본다.
- 실측: M-1 0:20.5~23초 기준일 카드가 4.85억·5.10억을 가림 잡음(첫 30초 오탐 0). G-1 실제 겹침 2건 잡아 고침. 부분만: `node work/video/ovcheck.mjs G1 g1.json out.json 0.5 3800-4300`.
- 새 부품을 만들면: 숫자 위에 카드·꼬리표를 띄우는 자리는 끝 이름표(선 그래프 series 이름)·0선 이름과 부딪히는지 overlap으로 한 번 잰다.

## 실사 장 머리(StockShot) 쓰는 법 — 장이 바뀔 때 2.5~4초 주제 실사 + 장 물음 (10/12, 사장님 10/11 "다른 애들도 다 장면 넣고 있구만")
1. 재료: `py -3.12 work/pexelsvid.py "<영어 검색어>" 4 work/research/longform/ep/<편>` → ep/<편>/stock/<id>.mp4(깃 제외) + credits.json(작가·주소·라이선스·desc_line). Pexels 라이선스 원문(10/12 확인): 영상 무료·출처 의무 없음·고쳐 써도 됨 / 금지 = 알아볼 수 있는 사람을 나쁘게, 사람·상표가 보증하는 듯, 원본 그대로 재판매.
2. 고르기(심사 1차 5·5에서 배운 것): **얼굴·국적·글자·숫자·연도·상표가 안 보이는 컷**만. 얼굴 있는 사람 위에 '깎임'류 제목을 얹으면 그 사람이 대상처럼 읽힌다(레드팀). 외국 거리 위 수명 숫자 = 그 사람 수명처럼 읽힘. 영문 달력 날짜 = 사실 날짜처럼 읽힘. 손·발·물건·풍경 클로즈업이 안전하다. 남은 상표는 `blur`(화면 1920x1080 좌표)로.
3. 재료 JSON: `shots[{seed·src('stock/<id>.mp4')·from(앞 자를 프레임)·chapter·title(대본 장 제목 그대로)·chip(facts 원문)·chipAt·dur·side·blur}]`. 예: `research/longform/ep/P-1/motion_preview/stockprops.py`(장 제목·칩 근거 assert, public/stock 복사, credits used 표시).
4. 미리보기: `npx remotion render src/motion/preview/entry.ts StockReel <out>.mp4 --props=<json> --scale=0.5 --pixel-format=yuv420p`
5. 본편: 장 첫 장면 앞에 `<StockShot {...shot} />`(TallyFrame 밖, 화면 전체) dur 105(3.5초) — 장 첫 말을 그 위에 깔면 dur를 그 줄 길이로(8초 넘기지 말 것 — U5). 설명란 끝에 credits.json desc_line(used=true) 줄을 붙인다.
6. 편마다 바뀜: 글자 쪽(한 편 안에서 번갈아 — side), seed로 밀어 들어가는 방향·제목 등장 방향·색 입힘(잉크/남색). 같은 컷을 다른 편에 다시 쓰지 않는다(credits.json used).

## 문턱 위 계단(StepCliff) 쓰는 법 — '선을 넘으면 툭 깎인다'(감액·과세 구간 문턱, 10/13 P-1 5장)
1. 재료 JSON: `seed·xMin·xMax·yMax·a·gap·cap·tiers[[초과 하한,그때 값,기울기]]·xticks·yticks·oldText·newText·plusText·zeroText·axisX·axisY·notWage·formula[]·salary·ask·jumpText·stair·pts[{x,text,at}]·capText·period·slips·zone·beats[15]`. 예: `research/longform/ep/P-1/motion_preview/stepprops.py`(곡선 식을 calc_out 점과 원 단위 assert).
2. 미리보기: `py -3.12 research/longform/ep/P-1/motion_preview/steprender.py`(원래 크기 렌더 + 줄마다 스틸 + motioncheck). 0.5배 렌더로 심사하지 않는다.
3. 규칙: 곡선은 식으로만(점은 calc_out과 맞는지 assert) · 원문 확인 안 된 옛 법 곡선은 그리지 않는다 · 가정(연금 월 100만원)은 세로축 제목에 늘 보인다 · 문턱 글자는 '이 선부터'(이상).
4. U5: beats = 말 줄 시작 프레임. 줄마다 왼쪽 빈 칸(문턱 아래 0원 구간 위)에 카드가 바뀌어 들어오고 카메라 초점이 옮겨 간다 → 58초 장면에 8초 넘는 같은 화면 0.
5. **SVG `<text>`는 카메라 변형(scale·translate) 안에서 렌더 프레임마다 자리가 어긋난다**(still은 정상, mp4만) — 축 눈금 같은 글자는 HTML div로 둔다.
6. 편마다 바뀜: seed로 왼쪽 여백·카드 기울기. 다른 문턱 주제(건보 피부양자·금융소득 2천만원 등)는 tiers·축만 바꿔 쓴다.

## 쇼츠 틀 c2person(C2P.tsx) 쓰는 법 — 장면마다 그림 1장 + 큰 3줄 자막 + 숫자 하나 (10/14, c1clip 10편 연속 ⓓ 막힘 풀기)
- 화면: 위 63%(1210px) 그림 꽉 채움(인물 가운데 cx, 켄 번스 zoom·pan·focus) · 고정 질문 2줄 · 주황 해 카드 · 오른쪽 위 가상 인물 배지 · 그림 아래 가장자리 흰 숫자 카드 1개 · 아래 어두운 칸 상자 없는 3줄 자막(숫자 노랑, red/green 낱말 색).
- props 만들기: research/cardshorts/c2s_jungwoo/c2pclip.py를 복사해 편 바꿈. sc(그림, 해 카드, [말 줄 앞부분], 숫자, 부제, zoom/pan/focus/gray/blur/red/green). 숫자·해는 말 줄·calc에 없으면 assert로 멈춘다. 장면 8초 넘으면 멈춘다.
- 렌더: `cd work/video && npx remotion render src/c2p_index.ts C2P out/<편>.mp4 --props=<편>.json` (약 4분/58초).
- 남의 돈·다른 사람 장면은 주인공 얼굴 위에 두지 않는다(blur: true + 해 카드에 '○○년 시작'). 배지는 '지수·환율은 실제, 통장은 계산'처럼 무엇이 계산인지 쓴다(레드팀 10/14).
- 반복 템플릿 피하기: 편마다 숫자 카드 위치(왼/오)·해 카드 색·그림 칸 높이를 바꿀 것(다음 편 할 일) — 같은 그림 6장으로 한 편 이상 만들지 않는다.

## 회사가 산 날들 vs 오늘 종가(BuybackDays) 쓰는 법 — 자사주·평균 매입가 비교(10/15 W-1 2화 2장)
1. 재료 JSON: `seed·days[{d,v}]·min·max·yticks·months·close·avg·lo·hi·card[머리,큰 금액,'A = B']·closeText·avgText·loText·hiText·first·last·total·allAbove·dotName·stemName·unsold·beats`. 예: `research/longform/ep/W-1/w1016/motion_preview/buyprops.py`(DART xml에서 하루 평균단가 바로 읽음, B9·B10·B11 assert).
2. 미리보기: `py -3.12 research/longform/ep/W-1/w1016/motion_preview/buyrender.py`(원래 크기 + 줄마다 스틸 2장 + motioncheck).
3. 규칙: 세로축이 0부터가 아니면 막대 금지 → 점 · 줄기 = 종가보다 높은 만큼(범례로 뜻 밝힘) · 가정 차이(회사 평균값에 샀다면 −318만원)는 화면에 내지 않는다 — 시청자가 내 손실로 읽음(심사 10/15) · 카드 한 칸에 기준 하나, 둘이면 구분선과 기준 글자.
4. U5: ① 점 날짜 순 찍힘 ② 종가 점선이 오른쪽에서 쓸며 줄기·최저·최고·검은 띠 ③ 점 흐려지고 평균선·카드. 편마다 seed로 왼쪽 여백.
