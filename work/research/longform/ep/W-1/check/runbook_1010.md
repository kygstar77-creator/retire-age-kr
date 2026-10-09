# W-1 녹음 순서 — 10/10 16:01 창 (PD, 10/9 18:3x 작성) — 회의가 10/10 창을 W-1에 줄 때만

전제: 10/10 06시 뒤 calc 재실행 → {F} 숫자 채움 → w1props 다시 → editor 재서명(말 줄 바뀌면 녹음 안 함). 빈자리({{·○) 남으면 make가 막는다.

## 요청 나누기 (`py -3.12 lfvoice.py plan research/longform/ep/W-1 --maxreq 9 --cap 270`, 10/9 확인)
| 요청 | 장 | 음절 |
|---|---|---|
| 1 | 0. 여는 장면 | 150 |
| 2 | 1. 이번 주는 사흘짜리 | 131 |
| 3 | 2. 첫 번째 영수증 | 377 (장 하나 — M-1 438 성공 범위) |
| 4 | 3. 두 번째 영수증 | 161 |
| 5 | 4. 세 번째 영수증 | 171 |
| 6 | 5. 세 장 합치기 + 6. 다음 주에 볼 날짜 | 265 |
| 7 | 7. 정리 | 180 |
7요청 → 여유 3(하루 10). {F} 갱신 뒤 음절이 바뀌면 plan 다시.

## 순서
1. `py -3.12 lfvoice.py make research/longform/ep/W-1 --maxreq 9 --cap 270 --gate 0.10 --budget 1 --first 1` → 0장만, 요청 음높이 줄 확인(기준 148Hz ±10%).
2. `py -3.12 lfvoice.py check research/longform/ep/W-1` 0장 줄·자르기 확인 → 통과면 W-1/tts.json에 "ref_f0": <0장 요청 음높이> 적기(다음 실행의 기준 — 실행마다 기준이 148로 돌아가는 것 막음).
3. `py -3.12 lfvoice.py make research/longform/ep/W-1 --maxreq 9 --cap 270 --gate 0.10 --budget 9` → 나머지 6 + 다시 받기 최대 3(벗어난 묶음만).
4. readback → (남는 요청 있으면 lfretake) → check(IQR ≤0.16·앞뒤 ≤7%·5.5↑) — 기준 낮추지 않음.
5. 통과: w1props → lfrender text(editor stamp) → lfrender render W-1 → 눈 검사 → scorecard → ytlong gate → 10/11 19:30 예약.
6. 미달: slots 칸 skip+사유, 녹음분 audio/w-1_1010 보관.
