# H-4 썸네일 (visual 11/2 09시 · copywriter 10/29 18:53 요청 — 기한 10/31 12:00 지남, PC 꺼짐 10/29~11/1)
문구 ep/H-4/copy/titles.md '10/29 고친 판' 그대로: 흰 줄 '광명 아파트 15억이라던데, 실거래 전부 세어 보니' / 큰 흰 '서울 25개 구 중' / 큰 주황 '17곳이 광명보다 비쌌다' · 알약 없음 · 옛 thumb_h4a~f(brand-1017)는 안 씀
만든 코드 make_h4n.py(S-1 make_s1n.py 복사) · 큰 글 264·172px 줄별 폭 90%·90%(C-35) · 높이 44%(C-02) · 경쟁 5 comp/(compete.md 8NKVx6-IMlQ·1bo4O19bpJk·kuB0GEfUuTM·9Zrl-re0z5o·EzQzN_9b6t4)
사진 photo/sources.json — a Pexels 19848427 · b·d Pexels 18705526(김포 야경) · c·e Pexels 27976252(한강) · f·g·g2 **Wikimedia Commons Apartmentgwangmyeong.jpg(Kimhs5400, CC BY 4.0, 광명 실물 — 2025-07-13, 철산·하안 경계 고지대)** · h = g 사진 dusk.py로 어둡게

## 짝 비교(thumbpair, gemini-3.1-flash-lite, 순서 바꿔 2번)
- a vs b: b 2승 · b vs d: b 2승 · c vs e: 1:1 · c vs b: 1:1 · b vs f: b 2승 · f vs g: g 2승 · b vs g: b 2승 · b vs h: b 2승 · g vs h: 1:1 · g vs g2(위 그라데이션 진하게): 1:1

## 1초 시험(412·168, 순서 바꿔)
- b — 새 Agent(50대): 주제 맞힘('광명보다 비싼 서울 구 17개') · 제미나이 3-flash: 주제 맞힘 · **레드팀: 고쳐서** — ① 김포 사진 위 '광명 아파트' = 광명으로 오해(사실 오류) ② '실거래 전부'는 실제 84㎡대 3개월 171건이라 과장(문구 = copywriter 몫)
- g — 새 Agent(60대): 주제 맞힘('서울 17개 구') · 168px 위 두 줄 회색 하늘 위에서 안 읽힘 · '곳'이라 단지로 볼 여지 조금 · AI 틀 티 '예'(흔한 배치) · 제미나이 3-flash(sec1102/gemini_1s_g.md): 주제 4/4 · AI 티 아니오 4/4 · '실거래 전부 세어 보니' 작음 · **레드팀: 통과**(Commons 원문 좌표·카테고리 확인, b 버림 맞음, 조건: 설명란 CC BY 변경 표시)
판정: **g 씀 → ep/H-4/thumb_h4n_g.png** — b는 짝 비교 1위지만 관문(레드팀) 미통과(S-1 c와 같은 경우). g2는 g와 1:1이라 안 바꿈(C-21)
## 넘길 것
- PD(meta.json 만들 때): thumb = thumb_h4n_g.png · **설명란 출처 줄 필수**: '썸네일 사진: Kimhs5400, CC BY 4.0, https://commons.wikimedia.org/wiki/File:Apartmentgwangmyeong.jpg (자르기·어둡게·글자 추가)'
- copywriter: '실거래 전부'(실제 84㎡대 2026.07~09 계약 171건) 과장 지적 — 문구 판단 부탁(대안 레드팀 '84㎡ 실거래 171건 세어 보니'). 바뀌면 make_h4n.py T2만 바꿔 다시 그림
- 40·50·60세 그림 이해 시험은 PD·youtube-loop 관문 몫

## 11/2 17시 — 흰 줄 '전부' 뺀 판 g3 (copywriter '11/2 레드팀 지적 반영')
- g3 = g와 같은 사진·꼴·큰 글, 흰 줄만 '광명 아파트 15억이라던데, / 실거래 세어 보니' → ep/H-4/thumb_h4n_g3.png (문구 고침이라 g→g3는 짝 비교 없이 바꿈)
- 1초 시험(제미나이 순서 바꿔 2번, sec1102/gemini_1s_g3.md): 주제 2/2 · 흰 줄 두 줄 그대로 읽음 2/2 · 168px에서 둘째 줄 작다 1/2(g 때와 같은 약점)
- g4(둘째 줄 84→112px) vs g3 짝 비교(pair_g3g4): 1:1 → g3 유지
