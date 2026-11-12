# p3s_cliff 관문 — firemap-video-producer 2026-11-12 (비축 — 쇼츠 reserve_min 2, 15:1x 비축 k1s_fix 1편 · 운영실장 15:10 '새 클립 1편(비주식·K-1 아닌 롱폼)')
| 관문 | 결과 | 근거 |
|---|---|---|
| 경쟁 비교 | 6편(Data API 조회순, 1위 214,237) · 제미나이 영상 보기 3편(1·2·4), 3·5·6은 429로 못 받음(확인 안 함) · 다른 한 가지 = 기준선 바로 위 한 칸의 실제 금액(166만원 0원 vs 167만원 매달 6만 8천원쯤) — 받은 3편 원 단위 보험료 0편 | compete.md |
| 틀 | c1clip(C1S live) · P-3 첫 클립 · 정책(건보료) 축, 주식 아님 · 11/12 k1s_dep(경제)·11/13 h3s_jeonse(부동산)·11/14 k1s_fix(경제)와 다른 축 | |
| 꼴 관문 ⓐ~ⓓ | 통과 — ⓐ 첫 줄 '기준은 한 해 소득 2천만원입니다.'(롱폼 질문 줄 63자는 35자 넘어 뺌) · ⓓ E-18 c1clip 998 vs 채널 996 | w1g1clips_check --form |
| 숫자 대조 | 화면·말 숫자 전부 P-3 calc_out·research·script와 일치, 못 찾음 0 | w1g1clips_check.py p3s_cliff (P-3 매핑 더함, 원본 .pre1112p3) |
| 새 녹음 | 0 — P-3 voice.json wav 9줄(1:1·1:2·0:5·0:6·0:7·2:19·2:24·2:8·8:1) | p3cclip.py |
| 답 위치 | 0초 질문 '국민연금 월 166만원과 167만원, 건보료는?' · 0원 5.6초 · 피부양자 빠짐 8.1초 · 6만 8천원 10.7초 | |
| 길이 | 32.3초 | |
| 이해 시험 | 3차 9명(40·50·60대) — 뜻·할 일 3/3, 권유 0, 3차 '167만원이면 피부양자 빠짐' 3/3 | understand.md |
| 쉿소리·음량 | deess --chirp-short · −17.0 LUFS · TP −1.5 | render_1112c.out |
| 안전 영역 | 33프레임 전부 안 — 첫 판은 계산기(calculator_hand)·달력(calendar_jan) 배경 숫자가 글자 상자로 10초 걸려 글자 없는 클립(apartment_windows·bench_backs·phone_pickup)으로 바꿈 | safezone.gate |
| 디자인 | 배경 실사 100%·자막 기준 100% | bgcheck.gate |
| 치직 | 0 | clickscan scan |
| 눈 검사 | sheet_1112.png(10장)·end_1112.png — 잘림·겹침·오타 0, 얼굴 0(뒷모습·손·봉투·아파트 항공), 배경 숫자·글자 0 · 손 동그라미가 '2.1% 오르면 기준 위'·'내년 2천만원 넘나' 글자 끝을 스침(k1s_fix와 같은 꼴, 읽기 지장 없음) | |
| 표지 | cover_1112.png(0.2초 질문 화면) | upload.json cover |
| 제목 | '피부양자 국민연금 월 167만원, 건보료 매달 7만원 가까이' 33자·숫자 2·검색어 맨 앞 | |
| AI 티 | 제목·설명 0.0(기준 12.0, 521자) · 면책 줄 '연금을 당기거나 미루라는 권유가 아닙니다.' | aitell desc_check.txt |
판정: 통과 (15:46 firemap-video-producer — 비축. 쓸 회차가 upload.json publishAt → w1g1clips_up.py p3s_cliff · mp4 work/video/out/p3s_cliff_c1_ds.mp4)
