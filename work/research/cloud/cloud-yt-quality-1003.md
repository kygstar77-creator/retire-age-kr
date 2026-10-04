# cloud/yt-quality-1003 — AI 유튜브 품질 스터디 + 시제품 2개 (2026-10-03)

## 무엇을 했나
- 2026-08-03 이후의 'AI로 유튜브 품질 올리는 법' 자료를 모아 정리했다. 분야는 6개다: 대본, 목소리, 화면, 썸네일, 편집 리듬, 쇼츠 첫 1초.
- 방법마다 우리 저장소(RULES.md, playbooks, workflow.md, work/video)와 대조해 새로움인지 이미 함인지 표시했다.
- 효과 순 상위 10과 분야별 출처표는 `work/research/ai-lab/study-2026-10-03-yt-quality.md`에 있다.
- 시제품 2개를 `work/video/src/motion-proto/`에 만들었다. motion/에는 다른 에이전트가 부품을 만들고 있어서, 코디네이터 지시로 폴더를 바꿨다.
  - `KaraokeCaption`(단어 강조 자막): `fm.Caption {s}` 자리에 그대로 넣으면 된다. 시간 계산은 `captionTiming.ts`가 한다.
  - `SayExact` + `speakWon`·`speakPct`(말은 반올림 숫자, 화면은 정확값 꼬리표): 계산은 `numberSpeech.ts`가 한다.
- 팀장이 예로 든 카운트업·막대 자라기는 **이미 있다**(fm.tsx `CountUp`, charts.tsx `BarSeries`·`Stairs`). 그래서 다시 만들지 않았다.
- 시험 결과
  - `node --test work/video/tests/yt_quality_proto.test.mjs`: 7개 통과
  - `work/tests/test_yt_quality_video.py`: 2개 통과(node 22.6 미만이면 건너뜀)
  - `tsc --strict` 타입 검사(스크래치 폴더에 remotion 4.0.532·react 19·typescript 5 설치): 통과
  - 새 .mjs의 eslint(저장소 설정): 통과

## 근거와 출처
- 우리 쪽 숫자
  - 대본 숫자 밀도 187 vs 경쟁 52(speechcompare.py)
  - E-2 f0 155→137Hz, 빠르기 최대 1.25배(RULES '목소리 한결같음')
  - 경쟁 화면 정지: 매경 최장 6.0초, 수페TV 23.8초(motioncheck.py)
- 원문을 읽은 외부 출처: [remotion-dev/skills](https://github.com/remotion-dev/skills)
  - timing: `Easing.bezier(0.16,1,0.3,1)`, 페이드 0.3*fps
  - transitions: 전체 = 장면 합 − 전환 합, `premountFor={fps}`
  - voiceover: 오디오 길이로 `calculateMetadata`
  - text-highlights: rough-notation
  - silence-detection: loudnorm → silencedetect d=0.5
  - display-captions
- 나머지 외부 출처는 전부 웹 검색 요약이다. 링크는 스터디 문서의 분야별 표에 있다.
  - Test & Compare 3안(노출당 시청 시간으로 승자 결정)
  - Gemini TTS: 긴 style 지시가 목소리를 흔든다, voice design 고정
  - 쇼츠: 0.8초 안 글자, 2~4초마다 변화
  - 첫 15초 가치 문장

## 확인 안 함
- **영상 본문·조회수 전부.** 이 작업실에서는 youtube.com과 대부분의 블로그·문서 사이트가 네트워크에서 막혔다(EGRESS_BLOCKED). vidIQ는 크레딧이 0이었고, 결제 금지 규칙 때문에 충전하지 않았다. 그래서 '조회수 상위 3~5편'은 고르지 못했다. 영상은 제목만 봤다.
- 검색 요약의 숫자(52% vs 44%, 1.8배, CTR 15~40% 등). 규칙으로 만들기 전에 실험 장부에 건다.
- Test & Compare를 우리 채널에서 쓸 자격과 API 가능 여부. Gemini 참조 음성을 무료 등급에서 쓸 수 있는지.
- 시제품의 실제 렌더. work/video에 package.json·src/index.ts·Weekly.tsx·Tour.tsx가 저장소에 없어 번들을 못 돌렸다. PC에서 `npx remotion studio`로 확인해야 한다.
- 단어 시각 어림(숫자 한 자리 1.5음절, %는 3음절, 말 구간 92%)과 실제 음성의 오차.

## 담당이 적용할 것
1. **카피라이터 + 영상 PD:** 다음 편 대본의 숫자 문장을 `speakWon`·`speakPct`의 say로 바꾼다. 같은 장면에 `<SayExact n={speakWon(값)} label="…" source="…" />`로 정확값을 띄운다. ① 브랜치(script-gate)의 '한 문장 숫자 1개' 기준과 같이 쓴다.
2. **영상 PD:** lfvoice에 `tts` 필드(숫자를 한글로 풀어 쓴 문장)를 추가하는 것을 검토한다. readback 실패와 재녹음을 줄이려는 것이다.
3. **영상 PD:** 롱폼 1편을 B군으로 정해 `KaraokeCaption`을 실험 장부(X-CAP-1 같은 이름)에 걸고, 7일 조회와 평균 시청 시간으로 판정한다.
4. **쇼츠 담당:** 7초 카드 절반을 '0프레임 완성 + 2초마다 한 가지 변화'(카운트 → PenMark → Drift)로 A/B한다. 판정 지표는 48시간 조회와 스와이프 이탈이다.
5. **카피라이터:** 다음 롱폼 공개 때 스튜디오 Test & Compare에 썸네일 3안을 건다. 사람 단계라 사장님이나 PC 세션이 해야 한다.
6. **개선 담당:** PC에서 `npx skills add remotion-dev/skills`를 설치한다. 새 부품을 `research/longform/loop/parts.md`에 기록한다(이 브랜치는 merge 충돌을 피하려고 parts.md를 건드리지 않았다).
