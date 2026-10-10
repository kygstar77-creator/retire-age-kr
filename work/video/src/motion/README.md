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
