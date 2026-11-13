# h4s_ladder 관문 — firemap-video-producer 2026-11-14 (11/18 19:20 칸, 비축 0이던 칸 · backlog ①)
| 관문 | 결과 | 근거 |
|---|---|---|
| 경쟁 비교 | 6편(Data API 8개 검색어·10/15 이후, 제미나이 영상 보기) · 다른 한 가지 = 같은 철산동 84㎡대 단지 16곳을 1년 실거래 가운데 값으로 줄 세움(맨 위 15.95억·맨 아래 6.35억, 1986년 주공13 13.85억 > 2009년 래미안자이 13.40억) — 경쟁 6편 중 같은 동 단지를 실거래로 줄 세운 편 0 | compete.md · compete_raw.json · compete_gemini.json |
| 틀 | c1clip(C1S live) · H-4 두 번째 클립(11/16 h4s_rank와 하루 띄움) · 부동산 축 — 쇼츠 실적 부동산 클립이 가장 높음(h1s_forest 1,732·h1s_gap 1,165, 11/14 Data API) | |
| 꼴 관문 ⓐ~ⓓ | 통과 — ⓓ E-18 c1clip 998 vs 채널 996 | w1g1clips_check --form |
| 숫자 대조 | 화면·말·설명 숫자 전부 H-4 calc_out §2·research와 일치, 못 찾음 0 | w1g1clips_check.py h4s_ladder |
| 새 녹음 | 첫 줄 1줄(Chirp 3 HD Charon 1.1·H-4 tts.json 같은 설정, f0 134.8Hz) — say '㎡' 그대로는 받아쓰기 '84M' → '팔십사 제곱미터'로 다시 받아 받아쓰기 일치 · 나머지 10줄 H-4 voice.json 4:2~4:11 그대로 | h4lclip.py |
| 이해 시험 | 3차 9명(40·50·60대) — 뜻 3/3·권유 0/3 · 1차 단지 이름 없음 → 칸에 이름, 2차 '16단지'(주공16단지로 읽힘)·'같은 동'(건물로 읽힘) → '단지 16곳'·'같은 동네' | understand.md |
| 윗줄 2배 시험 | 짝 비교 1:1 → 지금 판 유지(thumb-gap-1114 1위 지시) | toptest/pair_thumb.md |
| AI 티 | 제목·설명 0.0(기준 12.0) | aitell |
| 쉿소리·음량 | deess --chirp-short · −17.0 LUFS · TP −1.5 | deess_1114.log |
| 안전 영역 | 34프레임 전부 안 | safezone |
| 디자인 | 배경 실사 91%·자막 기준 100% · 0초 빈 곳 0% | bgcheck·emptyscan |
| 치직 | 0 | clickscan |
| 눈 검사 | sheet_1114.png(13장) — 1판 끝 장면(27~33초) 거리 실사 29354411에 사람 얼굴·가게 간판 → 항공 실사 37500921로 바꿔 뒤 토막만 다시 렌더 · 꽃밭 장면(3·12초)은 뒤로 아파트가 보여 둠 · 잘림·겹침·오타 0 | eye/ |
| 제목 | '철산동 아파트, 같은 동네 같은 크기인데 16억과 6억' 29자·숫자 2·검색어 맨 앞 | upload.json |
판정: 통과 (07:19 firemap-video-producer — 11/18 19:20 칸)
