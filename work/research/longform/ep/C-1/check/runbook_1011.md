# C-1 녹음 순서 — 10/11 16:01 창 (PD, 10/11 02:21 작성) — 15:05 배차 PD 회차가 쓴다

순돌이 10/11 02:08(a8fb416): C-1을 10/11 19:30로, 16:01 창 1요청으로 튀는 줄만 다시 받기, IQR 기준 0.20(앞뒤 7% 그대로).

## 왜 '튀는 3줄'만 받으면 안 되나 (02:2x 실측)
- 지금 voice.json: 80줄 · 10/09 68줄 + 10/10 12줄 · IQR 0.188(0.20 안) · 앞뒤 +3.6% · **튀는 줄 3**(0:0 190.5Hz · 8:0 191.2Hz · 9:1 205.1Hz, 허용 111.8~186.4).
- lfrender·lfvoice 날짜 규칙: 녹음 날이 **둘까지**, 둘째 날 줄이 20% 이하일 때만 허용(`retake_ok = len(ds) == 2`). 3줄만 10/11에 받으면 날짜가 10/09·10/10·10/11 셋 → **관문 거부**.
- 그래서 10/10 줄 12개(8:0 포함)와 10/09 튀는 줄 2개(0:0·9:1)를 합친 **14줄**을 10/11에 다시 받는다 → 10/09 66줄 + 10/11 14줄(17.5%, 20% 안).
- 기준은 손대지 않음. lfpitch 안 씀.

## 미리 잰 것 (TTS 0회, 모의)
| 새 14줄이 나온 음높이 | IQR | 앞뒤 차 |
|---|---|---|
| 140Hz | 0.143 | +0.9% |
| 149Hz | 0.136 | +1.8% |
| 160Hz | 0.140 | +2.9% |
| 170Hz | **0.206 막힘** | +3.9% |
남는 66줄: 중앙 148.1Hz, 117~183Hz. → 새 요청이 165Hz 밑이면 통과권.

14줄 · 약 322음절(`--cap 330` 안, 10/10 lfretake 15줄 1요청 성공 크기).

## 순서
1. `cp research/longform/ep/C-1/check/retake_must_1011.txt research/longform/ep/C-1/check/retake_must.txt`
2. `py -3.12 lfretake.py research/longform/ep/C-1 --n 0 --takes 1 --dry` → '다시 받을 줄 14(반드시 14·1번씩)' 확인
3. `py -3.12 lfretake.py research/longform/ep/C-1 --n 0 --takes 1` → 1요청. 반드시 줄이라 새 녹음으로 바뀐다(옛 것은 audio/c-1/_take_<시각>)
4. `py -3.12 lfrender.py voice research/longform/ep/C-1` → 날짜 {10-09: 66, 10-11: 14}·튀는 줄 0·IQR ≤0.20·앞뒤 ≤7%
   - 튀는 줄이 남으면: retake_must.txt를 **그 줄만** 남기고 `--takes 2`로 1요청 더(같은 10/11이라 날짜 규칙 그대로). 최대 3요청에서 멈춘다(G-1·W-1 몫 남김).
   - 날짜가 셋으로 나오면(새 줄이 build에서 rec 안 바뀜) 멈추고 기록.
5. `rm research/longform/ep/C-1/check/retake_must.txt` (다음 회차가 잘못 집지 않게)
6. readback(새 14줄) → `py -3.12 research/longform/ep/C-1/c1props.py` → `py -3.12 lfrender.py text research/longform/ep/C-1` → 화면 글자 바뀌면 editor 재서명(자막 줄은 말 그대로라 안 바뀔 것)
7. `py -3.12 lfrender.py render research/longform/ep/C-1` → 대표 프레임 5장 이상 눈 검사 → `py -3.12 video/chapters.py video/c1.json research/longform/ep/C-1`
8. meta desc: `desc_tpl`의 {CHAPTERS}·{CAFE} 채워 `desc` 칸 만들기(ytlong gate가 `desc`를 읽음 — 02:2x 건조 시험에서 KeyError 'desc'). {CAFE}는 카페 C-1 글이 아직이면 `https://cafe.naver.com/firemap`(M-1과 같음, 대본 '카페 firemap에' 약속과 맞음) → write가 22:10 칸에 올리면 그 주소로 videos.update
9. `py -3.12 ytlong.py gate research/longform/ep/C-1` → `up` → videos.list 확인 → uploads.jsonl·slots gates_ok(`date` 값)
10. 공개 직후 Studio: 고정 댓글(pinned_comment)·끝 화면 M-1

## 막히면
- 19:30 전에 4번을 못 넘기면 10/11 칸은 skip+사유, 녹음분 보관. 기준 낮추지 않음.
