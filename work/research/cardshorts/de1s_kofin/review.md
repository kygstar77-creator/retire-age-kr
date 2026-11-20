# de1s_kofin 관문 — firemap-video-producer 2026-11-20 (11/24 19:20 빈 쇼츠 칸, backlog ③)
| 관문 | 결과 | 근거 |
|---|---|---|
| 주제 범위(11/19 사장님) | 배당 ETF(국내 고배당 ETF 업종 쏠림) — 범위 안 | today.md 맨 위 |
| 주제 근거 | kwvol 11/20: PLUS고배당주 22,200 · SOL코리아고배당 7,760 · TIGER은행고배당플러스TOP10 3,980 · 고배당ETF 3,910 | compete.md |
| 경쟁 비교 | 7편(Data API 조회순·제미나이 영상 보기) · 다른 한 가지 = 국내 고배당 ETF 금융 비중을 같은 날 숫자로 맞대고 은행주 겹침을 짚음(경쟁 % 0편·겹침 0편) | compete.md |
| 틀 | c1clip(C1S live) · D-ETF-1 일곱째 클립 · 11/23 h2s_banpo(H-2) 다음이라 같은 롱폼 연속 아님 · 질문이 basket(SCHD↔국내 미국배당다우존스)과 다름 | |
| 꼴 관문 | 통과(1판 첫 줄 49자·숫자 없음 → 걸림 → 첫 줄 바꿈) · ⓓ E-18 c1clip 418 vs 964 '모든 틀 쉼 → 올림' | w1g1clips_check --form |
| 올리기 전 확인 | 11/20 네이버 증권 ETF 분석 다시(기준일 11/19): PLUS 금융 54.85→55.57 · SOL 45.8→56.40 · PLUS 맨 위 셋 같은 세 종목(2·3위 순서만 바뀜) — 화면은 새 값, 말은 그대로 맞음 | prepub_1120.txt · D-ETF-1 research.md '쇼츠 de1s_kofin 올리기 전 확인' · calc_kofin1120_out.txt |
| 숫자 대조 | 화면·말·제목·설명 숫자 못 찾음 0 | w1g1clips_check.py de1s_kofin |
| 녹음 | 롱폼 3:8·3:9·3:14 wav를 쉼(-40dB)에서 자름 + **새 1줄** 'PLUS 고배당주는 담은 돈의 55% 넘게가 금융이에요.'(Chirp 3 HD Charon·1.1·markup, D-ETF-1 tts.json 같은 설정, 3번 받아 f0 138.7Hz — 롱폼 자른 줄 129~148Hz 안) · 받아쓰기 gemini-3.8-flash 새 줄 2/2 글자 그대로 · 자른 롱폼 토막은 받아쓰기 429(롱폼 readback 10/22 통과분, 쉼에서만 자름) | stt.log · de1kclip.py |
| 이해 시험 | 5차 15명(43·54·63 / 46·57·66 / 41·52·62 / 44·55·64 / 42·53·65세) — 마지막 판 뜻·할 일 3/3, 권유 0/3 · 3·4차 'TIGER(은행 ETF) 99%를 나란히 놓아 과장' 6/6 → 새 첫 줄·TIGER 줄 뺌 | understand.md |
| 답 위치 | 0초 질문 '국내 고배당 ETF / 담은 돈은 어디에 있을까' · 0초 칸 'PLUS 고배당주 담은 돈의 55.6% 금융' · 첫 말 0.0초 숫자 | eye/f_0.3.png |
| 길이 | 16.8초 | |
| 쉿소리·음량·치직 | deess --chirp-short · -17.1 LUFS · TP -1.5 · 치직 0(렌더본·새 줄 wav) | deess_1120.log · clickscan |
| 렌더 | 1판(TIGER 맨 앞) 버림 · 3판 39494572 'No frame found' → cut 만들었으나 4판에서 safezone 걸림(휴대폰 주식 화면 속 글자 13상자·남의 차트) → 동전·공책 배경으로 바꾼 4판 | render_1120d.out |
| 안전 영역·디자인·0초 빈 곳 | 통과(17프레임 글자 상자 전부 안) · 실사 100%·자막 100% · 0% | safezone·bgcheck·emptyscan |
| 눈 검사 | sheet_1120.png(9장)·eye/cmp_circle.png: 얼굴 0·남의 차트 0·잘림·겹침 0 · 손 동그라미가 긴 값 양 끝 글자에 걸침 — DIVO 공개본(S-bh4F6JB-k)과 같은 꼴 · 공책 배경 손글씨(키릴 글자, 읽히지 않음) · 끝 출처 줄 보임 | |
| 표지 | cover_1120.png(2.0초 'PLUS 고배당주 / 담은 돈의 55.6% 금융') | upload.json cover |
| 제목 | '국내 고배당 ETF, 담은 돈 절반 넘게가 금융주였다' 해시태그 빼고 26자·숫자 0·검색어 '국내 고배당 ETF' 맨 앞 | |
| AI 티 | 제목·설명 0.0 · 설명란 '권유 아님' 줄 있음 | aitell·disclaim |
A-49: 답 첫 등장 0.0초 · 곁가지 0줄
판정: 통과 (firemap-video-producer 2026-11-20 10:59 — 11/24 19:20 칸 publishAt)
