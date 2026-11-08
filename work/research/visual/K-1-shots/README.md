# K-1 장면 (visual-designer 2026-10-26~27)
- `k1boards.py` 판 26장 → work/video/public/bg/k1/board/ (gitignore). 숫자 출처 ep/K-1/facts.txt F1~F25·raw/series.json.
- `ai_finish.py` AI 실사 7장(원본 bg/k1/ai_raw/, 생성 C:/Users/강영준/Documents/tools/localgen/k1/gen_k1.py, RealVisXL V5.0 openrail++) → bg/k1/ai/. 고른 시드·흐린 자리는 파일 안 J 표.
- `mkcmp.py` + `pick.json` 비교 그림 ep/K-1/shotcmp/rNN.jpg(경쟁 캡처 포함 — 커밋 안 함).
- `fill_plan.py` 심사 JSON → shot_plan.md 품질 판정 칸. 심사 기록 judge1_a/judge1_b(1차)·judge2(2차).
- 바꾼 것: r32 달력은 AI(가짜 숫자) → 종이 달력 판 k1_calendar · r37 끝 장면 Pexels 외국 집 → AI 한국 아파트 · r01·r12 Pexels 후보 없음 → AI.
- 11/8 23시 PD 실사 9컷(r38~r46): `mk1108b.py`가 비교 그림(경쟁 캡처는 옛 shotcmp 왼쪽 반 재사용). 새 심사관 판정 못함 → 같은 이름·길이로 클립 교체(원본 scratchpad, 인코딩 imageio_ffmpeg — remotion ffmpeg는 fps·setpts 필터 없음): news_cup 6975845 · money_count 5466763(1.206배 느리게) · money_pen 1188938 · notepad_calc 29303349 · water_drops 16648343 · dining_room 11099870. k1props STOCK id는 PD가 바꿈.
