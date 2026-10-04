# cloud/script-gate-1003 — 대본 검사기 보정 (클라우드 ①, 2026-10-03)

## 무엇을 했나
1. **speechcompare.py를 늘렸다** (work/research/longform/loop/speechcompare.py)
   - 지표를 더했다: 문장 길이 분포(평균·중앙·p90·표준편차), 숫자 개수 분포(0·1·2·3개 이상 문장 %), 숫자 하나 이하 문장 %, 반복 표현(세 번 넘게 나온 세 어절 묶음 %, 같은 머리 두 어절 최다), 접속사·추임새 종류 수와 빈도, 질문 문장 %. 원래 지표(-니다·-요, 숫자/1000단어, 숫자 2개 이상 %)는 그대로 뒀다.
   - `--loo`를 붙이면 지표 하나와 지표 둘(AND) 조합의 leave-one-out 정확도 표를 낸다. `--loo --write`는 가장 잘 가르는 조합을 research/editor/script_gate.json에 쓴다. 문턱은 경쟁 쪽 끝값이다.
   - 실행하는 폴더와 상관없이 돌도록 경로를 고쳤다.
2. **aitell.py에 대본 모드를 더했다**: `py -3.12 work/aitell.py --script <voice.json|script.md|txt>`. 통과면 0, 걸리면 종료코드 6이다.
   - 기준: 숫자/1000단어 ≤ 91.4 이고 숫자 2개 이상 문장 ≤ 20.4%.
   - script_gate.json이 있으면 그 기준을 먼저 쓴다.
   - 기존 모드(text·gate·pass·scan·frame·commaday, 파일 점수)는 손대지 않았다.
3. **근거 표**: work/research/editor/script-gate.md
4. **N-1 사람 말투 예시**: work/research/longform/ep/N-1/script.human-example.md
   - 말에는 반올림한 숫자 하나만 남겼다. 정확한 값은 `[자막: …]`으로 뺐다.
   - 원문 숫자는 모두 자막 표시에 남아 있다(테스트로 확인).
   - --script 결과는 **통과**다(87.4 · 3.7%). 읽는 말만 넣은 기존 AI 티 점수는 7.3으로 기준 12 안이다.
5. **테스트**: work/tests/test_script_gate.py, 10개 통과(`python3 -m pytest work/tests/test_script_gate.py`)

## 근거 숫자와 출처
| | 숫자/1000단어 | 숫자 2개 이상 문장 % | 출처 |
|---|---|---|---|
| 경쟁 사람 자막 12편 | 중앙 52 · 최대 91 | 중앙 11 · 최대 20 | meeting/today.md 413행(PC 10/3 speechcompare 실측) |
| 우리 E-1 / D-1 / E-2 / N-1 | 186.8 / 148.2 / 187.9 / 196.9 | 44.0 / 33.0 / 41.5 / 38.7 | 이번에 다시 잼(voice.json say) |
| N-1 예시 | 87.4 | 3.7 | 이번에 잼 |

- 우리 4편을 다시 잰 중앙값(187.35 · 40.1% · 111문장)은 PC 측정값(187 · 40% · 111)과 같다. 공식이 같다는 확인이다.
- LOO 정확도: 숫자 밀도 하나, 숫자 2개 이상 % 하나, 둘 다(AND) 모두 16/16 = 100%다. 이 값은 집계값에서 계산으로 끌어낸 것이다(유도 과정은 script-gate.md). 기존 aitell 점수는 6편 모두 0~3.5(기준 12)라 두 무리를 못 가렸다.

## 확인 안 함
- **경쟁 12편 자막 원본으로 돌린 LOO**: 이 작업실에서 www.youtube.com이 네트워크 정책에 막혔다(CONNECT 403). vidIQ 자막 도구는 크레딧이 0이었다. 그래서 subs/*.ko-orig.json3를 받지 못했다. 이 파일은 저장소 dev에도 없다.
- 문장 길이·질문형·추임새 종류·반복 표현이 사람과 우리를 가르는지: 경쟁 영상별 값이 없어서 규칙에 넣지 않았다.
- 자동 자막이 숫자를 글자로 적어 경쟁 숫자 밀도가 덜 세어졌을 가능성.
- 숫자를 줄인 대본이 조회나 시청 지속에 낫다는 증거.

## 담당이 적용할 것
- **youtube-loop / editor (PC)**: subs/가 있는 PC에서 `py -3.12 work/research/longform/loop/speechcompare.py --loo --write`를 돌린다.
  - 자막 원본으로 LOO 표를 다시 낸다.
  - script_gate.json을 만든다. 그러면 aitell이 그 기준을 쓴다.
  - 결과 표를 script-gate.md의 'LOO 정확도' 칸에 바꿔 넣는다. 값이 지금 기준(91.4 · 20.4)과 다르면 json이 이긴다.
- **youtube-loop**: 다음 롱폼(R-1)부터 녹음 전에 `aitell.py --script ep/<편>/script.md`를 돌린다. 종료코드 6이면 고친다. 고치는 틀은 N-1 예시를 본다: 금액과 등수를 두 문장으로 나누고, 반올림한 값 하나는 말로, 정확한 값은 `[자막: …]`으로.
- **video-producer**: `[자막: …]` 표시를 화면 자막이나 카드 글자로 옮긴다. TTS에는 넣지 않는다.
- **editor 참고 (기존 버그, 이번에 고치지 않음)**: aitell.score()에서 머리·꼬리 반복 루프 변수 `k`가 목록·법 문구 줄 수 `k`를 덮어쓴다. 그래서 '목록·법 문구 …줄은 끝맺음 반복에서 뺌' 안내가 엉뚱한 글자로 나온다. 점수는 바뀌지 않는다.
- 기존 AI 티 점수(파일 모드)는 `[자막: …]`, `(화면: …)` 줄도 문장으로 센다. 그래서 script.human-example.md 파일 자체는 12.3이 나온다. 읽는 말만 넣으면 7.3이다. 대본은 --script 모드로 본다.
