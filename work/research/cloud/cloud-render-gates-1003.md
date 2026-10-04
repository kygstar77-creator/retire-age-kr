# cloud/render-gates-1003 — 영상 화면 글자·목소리 렌더 관문 (클라우드 작업실, 2026-10-03)

지시: work/research/cloud-prompts-1003.md ②. 규칙 원문: work/research/longform/loop/RULES.md '화면 글자·그래프 규칙'·'목소리 한결같음'(둘 다 10/3 22시).

## 무엇을 했나
- **work/lfrender.py (새 파일)** — RULES '화면 글자' 3번에 적힌 "코드 관문은 lfrender에 붙인다"의 lfrender. 지금까지 렌더는 STATE.md에 적힌 `npx remotion render src/index.ts E1 out/e1.mp4 --pixel-format=yuv420p --props=e1.json`를 손으로 쳤고 Python 렌더 입구가 없었다. 그래서 관문 3개를 통과해야 같은 명령을 부르는 입구를 새로 만들었다.
  1. **화면 글자 뽑기·편집 통과 해시**
     - `text`: props(work/video/<편>.json)의 문자열 전부를 뽑는다. 그래프 제목·부제·출처·자막(lines.text)·막대 이름·레일이 들어간다. 컴포지션 tsx(예: N1.tsx)와 그 파일이 import하는 parts/*.tsx에 박힌 한글 글자(따옴표 문자열·JSX 글자, 주석 빼고)도 뽑는다. 결과는 `ep/<편>/screen_text.txt`.
     - 시각·절대경로·코드 줄 번호는 넣지 않는다. 화면 글자가 같으면 PC(Windows)든 클라우드든 같은 바이트가 나온다. 줄바꿈은 `\n`으로 고정했다.
     - `stamp`: editgate.py 방식으로 `screen_text.edit.json`을 찍는다. 내용은 `{by, at, sha=sha256(screen_text.txt 바이트), sha_of, note}`.
     - `render`·`check`는 늘 화면 글자를 **새로 뽑은 뒤** 해시를 대조한다. 표시가 없거나, 못 읽거나, sha가 없거나, 해시가 다르면 거부한다.
  2. **누적 구간 막대**: 장면(그래프 하나)마다 `data` 안의 문자열 가운데 `상위 N%`·`하위 N%`로 시작하는 이름을 모은다. `상위 1~10%`·`1~10%` 같은 구간 표기는 비누적이라 세지 않는다.
     - N이 서로 다른 이름이 2개 이상이면 경고한다.
     - 넓은 쪽 이름에 '포함'이 없으면 거부한다. 거부 문구는 RULES 1번 그대로 "겹치지 않는 구간으로 나누거나 '(상위 1% 포함)'을 적는다"이다.
  3. **목소리 한결같음**(voice.json의 줄마다 기록 기준):
     - f0가 그 편 중앙값 ±12% 밖이면 거부
     - tempo ≠ 1.0이면 거부
     - 녹음 날짜(`date`)가 2날 이상이면 거부. 주 녹음일이 아닌 줄을 목록에 올린다.
     - 다시 녹음할 줄은 `장:줄 | 문장 | 이유` 꼴로 출력한다.
- **work/lfvoice.py (조금 고침)**
  - `check` 끝에 같은 목소리 관문을 붙였다. RULES '목소리 한결같음'에 적힌 "lfvoice 검사에 붙임"이다. 이제 관문을 통과해야 '통과'가 나온다.
  - `build`가 wav를 처음 처리할 때(= make 직후) `.wav.json`에 `date`를 남기고, voice.json의 줄에도 `date`를 싣는다. 예전 파일에는 날짜를 지어내 넣지 않는다.
- **work/tests/test_lfrender.py (새 파일, 22개)**
  - 가짜 voice.json(정상·음높이 −13.3%·+11.3%는 통과·tempo 1.25·두 날·날짜 없음·f0/tempo 없음)
  - props 3종(비누적 통과 / 누적 거부 / '(상위 1% 포함)' 경고 후 통과)과 장면이 다를 때·하위·dict 이름
  - 화면 글자 관문(표시 없음 거부 → 찍으면 통과 → 제목을 바꾸면 거부, 코드 줄만 밀린 경우는 통과)
  - 거부 시 remotion을 부르지 않음 / 통과 시 정확한 명령
  - lfvoice.check에 연결됐는지(numpy가 있을 때만)

## 사용법
```
py -3.12 work/lfrender.py text   work/research/longform/ep/N-1                  # screen_text.txt 뽑기 → firemap-editor에게
py -3.12 work/lfrender.py stamp  work/research/longform/ep/N-1 firemap-editor "무엇을 봤는지"
py -3.12 work/lfrender.py voice  work/research/longform/ep/E-2                  # 다시 녹음할 줄 목록
py -3.12 work/lfrender.py check  work/research/longform/ep/N-1                  # 관문 3개만
py -3.12 work/lfrender.py render work/research/longform/ep/N-1 [remotion 추가 인자]   # 통과해야 npx remotion render N1 out/n1.mp4 …
python3 -m pytest work/tests/test_lfrender.py
```
우회 표시는 두지 않았다. RULES 3번이 "통과 전 렌더는 금지"이기 때문이다. 화면 미리보기(`node stills.mjs`)는 관문을 거치지 않으므로 화면 검사는 지금처럼 할 수 있다.

## 근거 숫자와 출처 (이 저장소 파일을 2026-10-03 클라우드에서 실측)
**실제 편에 관문을 돌린 결과**

| 편 | 누적 막대 | f0 중앙(허용 ±12%) | 음높이 밖 | tempo≠1.0 | 다시 녹음(합계) | 녹음 날짜 |
|---|---|---|---|---|---|---|
| A-1 | 없음 | 기록 없음 | – | 기록 없음 | 거부(f0·tempo 기록 없음) | 기록 없음 |
| E-1 | 없음 | 149.6 (131.6~167.5) | 20 | 19 (최대 1.463배) | 35/88 | 기록 없음 |
| D-1 | 없음 | 157.2 (138.3~176.0) | 10 | 9 (최대 1.25) | 17/70 | 기록 없음 |
| **E-2** | 없음 | **143.7 (126.5~160.9)** | **25** | **11 (최대 1.25)** | **32/67** | 기록 없음 |
| **N-1** | **거부: 장면 8 twin '받은 연봉 몫 vs 낸 세금 몫' — 상위 1%, 상위 10%** | 156.7 (137.9~175.4) | 10 | 18 | 24/46 | 기록 없음 |
| R-1(7/43줄만) | 없음 | 162.2 | 2 | 2 | 4/7 | 기록 없음 |

- 출처는 ep/*/voice.json의 줄별 `f0`·`tempo`와 work/video/*.json이다.
- 화면 글자 관문은 아직 어느 편에도 screen_text.edit.json이 없어서 6편 모두 '표시 없음'으로 거부된다.
- **E-2 목소리 모양**: 앞 절반 중앙 149.1Hz, 뒤 절반 138.1Hz다.
  - 장 4~6(자동차·규제 크레딧·비용)은 165~201Hz로 높게 튄다.
  - 장 9~11(주가·은퇴 계산·정리)은 110~126Hz로 낮게 튄다.
  - RULES의 "E-2 앞 155·뒤 137Hz"와 방향은 같다. 숫자가 다른 것은 앞뒤를 나눈 기준이 다르기 때문으로 보인다(RULES 쪽 나눈 기준은 확인 안 함).
- **N-1 누적 막대**: n1.json의 장면 8 `rows = [["상위 1%", 7.7, 30.3], ["상위 10%", 31.7, 71.7], ["아래 절반", 20.4, 1.43]]`. 사장님이 지적한 바로 그 그림을 관문이 잡는다.
- D-1은 RULES에 "159→157(정상)"으로 적혀 있지만, 줄 단위 ±12%로 보면 음높이 10줄이 밖이다. 앞뒤 평균은 고르지만 줄마다 튀는 것이 있다는 뜻이다.

## 확인 안 함
- **녹음 날짜**: 지금 voice.json 6편 어디에도 줄별 날짜 필드가 없다(필드: text·say·audio·sec·frames·rate·tempo·f0). 다른 자료로도 날짜를 알 수 없었다.
  - wav 파일 시각은 체크아웃 시각이라 쓸 수 없다.
  - git에서는 E-2 wav가 커밋 하나(2b935b16, 10/3 12:51)로 한꺼번에 들어왔다.
  - 그래서 '두 날 녹음' 검사는 실제 편에서 확인 안 함이다. 이 경우 관문은 거부하지 않고 '확인 안 함'만 출력한다.
  - 앞으로 lfvoice build로 새로 만드는 wav부터 date가 남는다.
- A-1은 voice.json에 f0·tempo가 없어서 음높이·빠르기를 확인 안 함(관문은 거부로 처리).
- 일부 wav가 저장소에 없다(예: work/video/public/audio/e-2/93cf7d07bd4cc01a.wav). 그래서 `lfvoice.py check E-2` 전체(wav를 다시 재는 부분)는 클라우드에서 못 돌렸다. 관문 값은 voice.json에 기록된 f0·tempo로 냈다.
- 썸네일 문구는 그림(png)이라 screen_text.txt에 들어가지 않는다. RULES 3번은 썸네일 문구도 편집 관문 대상이라고 한다 → 썸네일 문구 원본 파일이 정해지면 붙인다.
- tsx 글자는 템플릿 문자열 안의 식(`${n0(d.avg)}만원`)이 값이 아닌 식 그대로 뽑힌다. 실제 값은 props 쪽 숫자로 본다.
- `npx remotion render`를 실제로 돌리지는 않았다(src/index.ts가 저장소에 없고 node_modules도 없음). 명령 문자열만 테스트로 확인했다.
- ±12%·tempo 1.0·한 날 녹음은 RULES 10/3 22시 사장님 지시를 그대로 옮긴 값이다. 12%의 근거 실측은 확인 안 함.

## 담당이 적용할 것
- **video-producer**
  - 렌더는 `lfrender.py render <ep>`로만 한다.
  - `lfvoice.py`의 `tempo()`가 아직 5.6음절/초 밑이면 atempo로 최대 1.25배까지 늘인다. 이대로 만들면 관문에 걸리므로 RULES ② "빠르기 고정, 장면 길이를 목소리에 맞춘다"대로 tempo()를 1.0 고정으로 바꾼다. 같은 이유로 `check`의 '느림(5.6 미만)' 기준도 함께 다시 정한다(규칙이 서로 부딪힘).
  - E-2·N-1은 이미 예약·공개됐거나 공개가 정해져 있다. 다시 녹음할지는 위 목록(`lfrender.py voice`)으로 판단한다. 다음 편(R-1)은 한 날 한 회차에 녹음한다.
- **firemap-editor**: 렌더 전에 `lfrender.py text`로 뽑은 screen_text.txt를 RULES 4번 질문("사람이 소리 내 말할 때 이렇게 말하나? 오해할 그래프는?")으로 보고 `stamp`를 찍는다.
- **N-1 화면 담당**: n1props.py 장면 8의 '상위 10%'를 '1~10%'(누적값을 빼서 계산하고 계산식은 facts.txt에) 또는 '상위 10% (상위 1% 포함)'으로 바꾼다.
- PC의 cloudmerge.py가 합친 뒤 `python3 -m pytest work/tests/test_lfrender.py` 22개가 통과하는지 확인한다.
