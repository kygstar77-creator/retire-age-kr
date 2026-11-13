# h3s_number 관문 — firemap-video-producer 2026-11-13 (11/15 19:20 칸)
| 관문 | 결과 | 근거 |
|---|---|---|
| 경쟁 비교 | 6편 — 다른 한 가지 = 같은 60㎡대 평당 중간 가격으로 단지(7 vs 11 30%)·앞/뒤 번호(20%) 맞댄 편 0 | compete.md |
| 틀 | c1clip(C1S live) · H-3 두 번째 클립(h3s_jeonse 11/13과 이틀) · 부동산 축 | |
| 꼴 관문 | 통과 — ⓓ E-18 c1clip 998 vs 채널 996 | w1g1clips_check --form |
| 숫자 대조 | 화면·말·설명 숫자 전부 H-3 원문과 일치, 못 찾음 0 | w1g1clips_check.py h3s_number |
| 새 녹음 | 0 — H-3 voice.json 그대로 | h3nclip.py |
| 답 위치 | 0초 질문 '같은 평수인데, 단지 번호 따라 값이 다를까?' · 30% 4.5초(손 동그라미) | f045_1113.png |
| 길이 | 51.5초 | |
| 이해 시험 | 2차 3/3(40·50·60세) 통과 | understand.md |
| AI 티 | 제목·설명 0.0(기준 12.0) · 면책 '사거나 팔라는 권유가 아닙니다.' | aitell |
| 쉿소리·음량 | deess --chirp-short · −17.0 LUFS · TP −1.3 | deess_1113.log |
| 안전 영역 | 52프레임 전부 안 | safezone |
| 디자인 | 배경 실사 100%·자막 기준 100% · 빈 곳 최대 0% | bgcheck·emptyscan |
| 치직 | 0 | clickscan |
| 눈 검사 | sheet_1113.png(3초 간격 18장)·f00·f02·f045·end_1113 — 잘림·겹침·오타 0, 얼굴 0(손·건물·서류) | |
| 렌더 | 02:39·06:21 회차는 빈 메모리 0.2~0.3GB로 No frame found → 14:16 빈 메모리 2.15GB에서 3토막 한 번씩에 통과 | render_1113_1416.out |
| 표지 | cover_1113.png(5.2초 '7단지가 30% 높음' 동그라미) | upload.json cover |
| 제목 | '목동신시가지, 같은 평수인데 단지 따라 평당 30% 차이' 해시태그 빼고 30자·숫자 1·검색어 맨 앞 | |
판정: 통과 (14:40 firemap-video-producer — 11/15 19:20 칸 publishAt)
