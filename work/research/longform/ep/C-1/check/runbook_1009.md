# C-1 녹음 순서 — 10/9 16:01 창 (PD, 10/8 22:2x 작성)

근거: today.md 회의 10/8 21:45 [지시] PD(250음절 안팎·80% 넘기 전 1요청 시험) · lessons 24 · lfvoice.py `--cap`(10/8 22:19 추가).

## 요청 나누기 (API 안 부르고 확인함: `lfvoice.py plan research/longform/ep/C-1 --maxreq 9 --cap 270`)
| 요청 | 장 | 음절 |
|---|---|---|
| 1 | 0. 여는 장면 | 290 |
| 2 | 1. 두 사람의 규칙 | 169 |
| 3 | 2. 첫해 영수증 | 248 |
| 4 | 2-2. 매도 씨 영수증 + 3. 평균이면 둘 다 평생 | 262 |
| 5 | 4. 실제 순서로 돌리면 | 193 |
| 6 | 5. 두 해 따라가기 | 228 |
| 7 | 6. 꺼내는 돈을 바꾸면 | 153 |
| 8 | 7. 환율이 받쳐 준 해 | 223 |
| 9 | 8. 정리 | 213 |
합 1,979음절·75줄 · 9요청 = 하루 한도 10의 90% → 1요청 시험 먼저. 남는 1요청은 lfretake 몫.
- 0장 290은 장 하나라 더 못 쪼갬(헤더를 새로 넣으면 대본 변경 = youtube-loop·editor 몫). 실측 근거: M-1 438음절 묶음 자르기 성공, G-1 519음절 실패 → 290은 안전 쪽.
- 기본 --cap 없이 --maxreq 9로 돌리면 7+8장이 436음절로 묶인다 — 반드시 --cap 270.

## 순서
1. 16:00 전: `py -3.12 work/editgate.py`류 대신 확인 — script.md 말 줄은 editor 통과(32d14ea) 뒤 바뀐 것 없음(65ae31e는 `## 2-2` 머리만 추가, 10/8 22:2x diff 확인). 그 뒤 바뀌었으면 녹음하지 않는다.
2. 16:01 `py -3.12 work/lfvoice.py make research/longform/ep/C-1 --maxreq 9 --cap 270 --first 1` → 0장만.
3. `py -3.12 work/lfvoice.py check research/longform/ep/C-1` 의 0장 줄 f0 중앙·속도 확인(기준: 다른 편 144~157Hz, 편 전체 5.5↑) + 자르기 성공 여부. 
   - 자르기 실패/첫 문장 ⚠ → fixcut 0 (API 아님, 받아쓰기만) 후 다시 확인. 음높이 130Hz대면 멈추고 사유 기록(10/10 칸 skip 판단).
4. 통과면 `--first` 없이 같은 명령 → 나머지 8요청(이미 받은 0장은 다시 안 보냄).
5. readback → lfretake(1요청, 튀는 줄만) → check 통과 → 이후는 meta.json todo_pd 순서(c1props → lfrender text → render → ...).
6. check 못 넘으면: 기준 낮추지 않음. slots 10/10 19:30 칸 skip+사유(G-1은 다시 녹음 전이라 대체 불가) → today.md·decisions/log.md.
