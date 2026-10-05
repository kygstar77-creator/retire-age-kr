# R-1 16:00 녹음 순서 (PD 2026-10-05 06:3x 작성 — 클라우드 리메이크 확정 af2eeaa 뒤)

대본 = script.md(= script.v6.md, 클라우드 최종, 말 153문장). 10/5 03:21 녹음 150문장은 PC v6 대본 것이라 **다시 쓸 문장 0**(문장 해시 일치 0) → 전부 새로 녹음. 한 날 규칙: 10/5 16:00~24:00 안에 끝낸다.

## 전제
- [ ] firemap-editor 편집 통과: script.md sha256 5bdda789… 로 .edit.json 다시 찍힘(지금 .edit.json은 PC v6 36dbfda… — 불일치). 자막 [자막] 63줄 포함.
- [ ] TTS 할당량 16:00 KST 초기화(무료 모델당 하루 10회). 계획 = 9회(묶음 9).

## 명령 (work 폴더에서)
1. `py -3.12 lfvoice.py make research/longform/ep/R-1 --maxreq 9 --first 1`   # 첫 묶음 1회만
2. `py -3.12 lfvoice.py check research/longform/ep/R-1`   # 녹음된 문장만 f0 보기(남은 문장 때문에 '막힘'은 정상)
   - 첫 묶음 f0 ±12% 밖이 10% 이하 → 3으로.
   - 넘으면: research/longform/ep/R-1/tts.json에 `"prompt": "Read these Korean lines in order as a steady YouTube finance narration with an even, consistent pitch. Keep a quick, constant pace. Pause briefly between lines:\n"` 추가 → 첫 묶음 wav를 audio/r-1_try1/로 옮김 → 1·2 다시(요청 1회 더, 합계 10회 — 남는 요청 없음).
3. `py -3.12 lfvoice.py make research/longform/ep/R-1 --maxreq 9`   # 나머지 8회
4. `py -3.12 lfvoice.py check research/longform/ep/R-1` → 통과(f0 ±12%·한 날·5.5음절/초 이상)
5. `py -3.12 lfvoice.py readback research/longform/ep/R-1` → 걸린 문장 0 (받아쓰기 429면 LFCUT_MODELS lite)
6. `py -3.12 research/longform/ep/R-1/r1props.py --script script.md` → missing 0
7. 렌더 → deess → `py -3.12 video/motioncheck.py <mp4>` → scorecard → `ytlong gate`

## 오늘 아침 측정(옛 PC v6 녹음 150, voice_check_1005am.txt)
- f0 중앙 153Hz, 묶음 안 표준편차 12~31Hz(101~226Hz), ±12% 밖 78(옛 자기상관)·85(YIN) — 두 방식 다 비슷 → 측정 오류 아님, 실제 높낮이 흔들림.
- 같은 모델·목소리·지시문으로 N-1·E-2는 0건 → 날·요청마다 다름. 그래서 첫 묶음 1회 뒤 바로 check.
- 편 전체 7.27음절/초(규칙 기준 5.65 고정 대비 빠름) — 'energetic, brisk' 지시문 영향 의심(확인 안 함).

## 10/6 16:01 추가 — 녹음 뒤 음높이 맞춤 길(PD 10/5 18:17 시험, work/lfpitch.py)
- 10/5 녹음 153줄로 시험: `py -3.12 lfpitch.py make research/longform/ep/R-1 --target 136 --trim 0.1` → 편 단위 앞뒤 차 +8.3%→+3.0%·퍼짐 0.22→0.08·편 전체 5.44→6.14음절/초 = **음높이·전체 속도 기준은 통과**. 남는 막힘은 줄 속도 27(빠름 26: 2장 9~10음절/초, 느림 1) — 빠르기는 고정이라 이건 다시 녹음 몫.
- 옮김 한도 ±15%: ×1.35로 옮기면 받아쓰기 일치 0.83→0.64까지 떨어짐, ×1.15에선 8줄 중 6줄 그대로(1줄 0.67·1줄 받아쓰기 실패). 공개 전 맞춤 사본도 readback 필수.
- 10/6 순서: 1~3 그대로(153줄 한 날) → 4 check가 **음높이(drift·iqr·±25%)로만** 막히면 `lfpitch.py make ... --trim 0.1` → 통과하면 voice.json을 voice.orig.json으로 남기고 voice_pitch.json을 voice.json으로 → readback → 6·7. 줄 속도로 막히면 그 줄만 남은 요청(같은 날)으로 다시.
- 맞춤 사본을 공개에 쓰는 건 이번이 처음 — decisions/log.md에 적고, 공개 뒤 사장님 지적 오면 바로 멈춤.
