# G-1 녹음 순서 — 10/11 16:01 창 (PD, 10/10 18:26 작성) — 운영실장 15:05 배차 회차가 쓴다

전제: 대본 말 줄은 editor 통과본(script.md.edit.json 10/9 07:06) 그대로. 말 줄이 바뀌었으면 녹음 안 함.
화면 글자: 10/10 PD가 motion 부품 3개(BuyDateOpen·WaterfallPieces·AsymClimb)를 G1.tsx에 끼워 screen_text가 바뀜 → editor 재서명 필요(today.md 요청). 렌더 전까지면 되고 녹음과는 무관.

## 요청 나누기 (`py -3.12 lfvoice.py plan research/longform/ep/G-1 --maxreq 9 --cap 330`, 10/10 확인)
| 요청 | 장 | 음절 |
|---|---|---|
| 1 | 0. 여는 장면 + 1. 오늘 금값 한 장 | 312 |
| 2 | 2. 산 날 영수증 4장 | 176 |
| 3 | 3. 국제 금값과 내 금이 | 249 |
| 4 | 3-2. 고점·3개월 전 | 164 |
| 5 | 4. 산 길 4개 | 240 |
| 6 | 4-2. 골드뱅킹과 골드바 | 279 |
| 7 | 5. 같은 시기에 움직인 | 279 |
| 8 | 6. 산 값까지의 산수 + 7. 정리 | 277 |
8요청 → 다시 받기 여유 2(하루 10). cap 300은 9요청·여유 1, cap 270은 10요청이라 막힘. 312음절은 M-1 438 성공 범위 안.

## 순서
1. `py -3.12 lfvoice.py make research/longform/ep/G-1 --maxreq 9 --cap 330 --gate 0.10 --budget 1 --first 1` → 요청 1만. 음높이 기준 148Hz ±10%(10/8 G-1 장 중앙 138~189Hz).
2. `py -3.12 lfvoice.py check research/longform/ep/G-1` → 0·1장 자르기·readback 확인. 통과면 G-1/tts.json에 "ref_f0": <요청 1 음높이>.
   - W-1 10/10 교훈: 첫 요청이 128Hz로 낮게 나와 2요청을 버렸다. 첫 요청이 ±10% 밖이면 **한 번만** 다시 받고, 또 밖이면 가장 가까운 것을 ref로 삼고 진행(예산이 다음 장을 못 받게 되는 게 더 큰 손해).
3. `py -3.12 lfvoice.py make research/longform/ep/G-1 --maxreq 9 --cap 330 --gate 0.10 --budget 9` → 나머지 7 + 다시 받기 최대 2.
4. readback → check(IQR ≤0.16·앞뒤 ≤7%·5.5↑). 기준 낮추지 않음, lfpitch 안 씀.
5. 통과: `py -3.12 research/longform/ep/G-1/g1props.py`(motion 3개 자동으로 다시 맞춤) → lfrender text → (글자 바뀌었으면 editor stamp) → `py -3.12 lfrender.py render research/longform/ep/G-1` → 첫 장면·3장·6장 motioncheck(최장 정지 3초 이하, motion.md 요청 2) → 대표 프레임 눈 검사 → scorecard → ytlong gate → 10/13 19:30 예약.
6. 미달: slots 10/13 칸 skip 판단은 관문 기한(10/12 19:30) 때 — 녹음분 audio/g-1_1011 보관.

## 붙는 확률(정직하게)
- 10/8 G-1 녹음분의 **장 안 퍼짐만 0.175**(요청마다 중앙을 완벽히 맞춰도 0.16 초과). 같은 대본·같은 목소리면 이번에도 넘기 어렵다(근거 C-1/check/pitch_drift_1009.md '10/10 판정').
- 그래도 녹음하는 이유: 요청마다 흔들림이 달라 0.16 밑으로 들어올 수 있음(M-1 36글자 편 0.133 통과), 창을 비우면 G-1·C-1·W-1 셋 다 0편.

## 10/10 18:26 준비 끝(PD)
- g1props.py swap_motion: motion_preview 세 스크립트를 voice.json 길이로 돌려 open·wf1·math 장면 자리에 끼움(문장이 PD 장면과 한 줄이라도 다르면 멈춤). 장면 28→26·종류 20.
- 스틸 video/out/g1_stills_1010 눈 검사: 3장 0선 이름표가 화면 왼쪽 끝에 잘림 → WaterfallPieces 왼쪽 맞춤 · 6장 '수수료…' 도장이 카메라 1.08배일 때 분홍 테두리에 겹침 → AsymClimb 두 줄·오른쪽. 그 밖 잘림·겹침 0.
