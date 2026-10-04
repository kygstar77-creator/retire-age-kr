# AI로 유튜브 만들 때 품질 올리는 법 — 스터디 (2026-10-03, 클라우드 작업실 ④)

브랜치 `cloud/yt-quality-1003`. 범위는 2026-08-03 이후 유튜브 영상과 글이다. 한국어를 먼저 찾고 영어도 함께 봤다.

## 먼저 밝혀 둘 한계 (읽기 전에)
- **영상 내용을 직접 보지 못했다.** 이 작업실에서는 youtube.com, remotion.dev, substack, huggingface, brunch 등 대부분의 사이트가 네트워크에서 막혔다(WebFetch가 EGRESS_BLOCKED). vidIQ도 크레딧이 0이라 한 번도 부르지 못했다. 결제를 하지 않는다는 규칙이 있어 충전도 하지 않았다.
- 그래서 근거는 두 갈래뿐이다.
  - **웹 검색 결과 요약.** 표에는 `검색 요약만 봄`으로 적었다. 이건 '설명란만 봄'보다도 약한 근거다. 검색 도구가 만든 요약이라 어느 숫자가 어느 글에서 나왔는지 섞여 있을 수 있다.
  - **GitHub 원문.** remotion-dev/skills는 원문을 직접 읽었다. 표에는 `원문 봄`으로 적었다.
- **조회수·참여로 매긴 '상위 3~5편' 순위는 확인 안 함.** 조회수를 잴 길(vidIQ, 유튜브 페이지)이 막혔다. 분야마다 검색 상위에 나온 것을 골랐다. 날짜도 검색 요약에 나온 것만 적었고, 나머지는 '확인 안 함'이다.
- 검색 요약의 숫자(예: "첫 15초 가치 약속 52% vs 44%")는 글쓴이가 낸 숫자다. 우리 채널에서 재 본 값이 아니다. **규칙으로 만들기 전에 실험 장부(longform/loop/experiments.md)에 걸어 우리 숫자로 판정한다.**

## 우리 현재 상태 (대조 기준)
| 항목 | 지금 | 근거 |
|---|---|---|
| 대본 숫자 밀도 | 1,000단어당 187개(경쟁 52, 최대 91) → 3.6배. 숫자 2개 이상 든 문장은 우리 40%, 경쟁 11% | longform/loop/speechcompare.py, cloud-prompts-1003 ① |
| 목소리 | 날을 나눠 녹음해서 E-2 뒤쪽 f0가 155Hz에서 137Hz로 내려갔다. 빠르기를 1.25배까지 바꿨다. 관문 규칙은 정했지만 코드는 ② 브랜치에서 작업 중이다 | RULES.md '목소리 한결같음' |
| 길이 | 롱폼 6~9분(A-1만 15분). 쇼츠는 7초 정지 카드이고, 첫 1초가 그림인 편이 잘됐다 | RULES '롱폼 길이 관리', playbooks/firemap-shorts.md |
| 화면 | Remotion(work/video). CountUp(fm.tsx), 막대 자라기(charts.tsx BarSeries·Stairs), HookNumber, Beat(6초 시선 이동), PenMark, Wipe(beats.tsx), 정지 화면 관문 motioncheck.py(정지 15초 이하) | research/longform/loop/parts.md |

→ 팀장이 예로 든 **숫자 카운트업과 막대 자라기 부품은 이미 있다**(`parts/fm.tsx` CountUp, `parts/charts.tsx` BarSeries가 `appear(p*60, i*4, 30)`로 차례로 자람). 다른 에이전트(R-1 리메이크)도 `work/video/src/motion/`에 일반 부품을 만들고 있다. 그래서 시제품은 겹치지 않는 두 가지로 만들었다(아래 '시제품').

---

## 효과 순 상위 10
효과를 매긴 기준은 하나다. 지금 우리 약점(숫자 밀도, 목소리, 정지 쇼츠)을 얼마나 직접 고치나. 출처 숫자의 크기는 기준으로 쓰지 않았다(검증 전이다).

| # | 방법 | 담당 | 바꿀 것 | 기대 효과 | 비용 | 위험 | 우리 |
|---|---|---|---|---|---|---|---|
| 1 | **말은 반올림한 숫자 하나, 정확한 값은 화면 꼬리표** | 카피라이터(대본), 영상 PD(화면) | voice.json `say`에는 `speakWon()`·`speakPct()`의 반올림값을 쓴다. 장면에는 `SayExact`로 사실표 정확값을 '정확히 …' 꼬리표로 띄운다 | 숫자 밀도 187 → 경쟁 범위(≤91)로 내려가도 화면 정확도는 그대로 | 낮음(시제품 있음) | 반올림 말과 정확값이 달라 보일 수 있다 → 꼬리표가 늘 같이 뜨고, '약'을 붙인다 | **새로움**(시제품 `motion-proto/`) |
| 2 | **첫 15초 안에 구체적 가치 문장 하나**(3단 오프닝: 패턴 깨기 → 보상 약속 → 끝까지 볼 이유) | 카피라이터, 대본 관문(aitell) | 대본 첫 3문장 안에 '이 영상에서 얻는 숫자·답'을 한 문장으로 넣는다. aitell 대본 모드에 '15초(약 85음절) 안 가치 문장 있음' 검사를 넣는다 | 30초 유지율. 출처 주장은 52% vs 44%이고 확인 안 함 | 낮음 | 낚시 문구가 될 수 있다 → 권유 금지 규칙 그대로 | **일부 이미 함**(E-2의 '믿기 어려운 한 줄 → 곧바로 공식 증거'). 15초 검사는 새로움 |
| 3 | **쇼츠 7초 카드를 0프레임부터 완성하고, 2초마다 한 가지씩 바꾸기** | 쇼츠 담당 | 0프레임에 그림과 큰 글자가 이미 떠 있게 한다(페이드인 금지). 0~1.2초 숫자 카운트, 2~3초 핵심 칸 PenMark, 4~5초 Drift 1.03배, 6초 꼬리 한 줄 | 1초 유지(스와이프 이탈). 출처는 '0.8초 안 굵은 글자', '정지 슬라이드는 스와이프당함', '2~4초마다 변화'(확인 안 함) | 중간(cardshort.py 출력 또는 Remotion 쇼츠 틀) | 7초 표 한 장이 이미 잘된 틀이다 → '터진 형식은 지킨다' 규칙대로 절반만 A/B | **새로움**(롱폼 beats는 있고, 쇼츠 카드는 정지다) |
| 4 | **TTS에 넣는 숫자를 한글로 풀어 쓰기** | 영상 PD(lfvoice) | voice.json에 `tts` 필드를 둔다(`4,475만원` → `사천사백칠십오만 원`). 화면·자막은 `say` 그대로 | 숫자를 잘못 읽어 다시 녹음하는 일이 줄어든다(E-1에서 "6.5배"를 "6배"로 읽었다). 재녹음이 줄면 다른 날 녹음이 섞일 일도 준다 | 낮음 | 풀어 쓰기 함수가 틀릴 수 있다 → readback 대조는 계속한다 | **새로움**(지금은 숫자를 그대로 보내고 readback으로 사후에 잡는다) |
| 5 | **목소리를 고정 참조로 묶고 지시문은 짧게** | 영상 PD | Gemini TTS의 voice design·참조 음성으로 한 목소리를 저장하고 그 ID만 쓴다. style은 한 줄로 쓴다. 쉼은 `<short pause>` 태그로 넣는다 | 날마다 목소리가 달라지는 문제 완화 | 낮음~중간. 무료 등급 지원은 확인 안 함 | 출처는 Google 문서 요약이고 실측 전이다 → 같은 문장을 이틀 녹음해 f0 차이로 판정한다 | 짧은 영어 지시문·한 회차 녹음은 **이미 함**. 참조 음성 고정은 **새로움** |
| 6 | **유튜브 Test & Compare로 썸네일·제목 3안 시험** | 카피라이터, 영상 PD | 공개할 때 스튜디오(데스크톱)에서 썸네일 3안 또는 제목+썸네일 3안을 건다. 승자는 '노출당 시청 시간'으로 정해진다 | 수동 교체(X-THUMB)보다 같은 기간에 공정하게 비교. 출처 주장은 CTR 15~40% 향상(확인 안 함) | 낮음(무료 기능) | 채널 자격과 API로 걸 수 있는지는 확인 안 함 → 사람(스튜디오) 단계가 필요할 수 있다. '72시간 교체 금지'와는 충돌하지 않는다(공개 때부터 걸기 때문) | **새로움**(저장소에 Test & Compare 언급 0건) |
| 7 | **단어 강조 자막**(지금 읽는 어절만 밝게) | 영상 PD | 새 편에서 `fm.Caption`을 `KaraokeCaption`으로 바꿔 끼운다(쇼츠는 maxChars 14~16) | 자막을 따라 읽게 해 시선을 붙잡는다. 출처 주장은 '애니메이션 자막이 정지 자막보다 참여 높음'(확인 안 함) | 낮음(시제품 있음) | 정보형 채널에서는 산만할 수 있다. 단어 시각이 어림값이다 → 롱폼 1편만 B군 | **새로움**(시제품) |
| 8 | **문장 길이에 변화 주기**(짧은 문장과 긴 문장 섞기) | 카피라이터 | 문장 길이 분산을 aitell 대본 점수에 넣는다 | 출처 주장은 균일한 문장보다 유지율 1.8배(확인 안 함) | 낮음 | — | ① 브랜치(cloud/script-gate-1003)에서 **진행 중**이라 여기서는 안 했다 |
| 9 | **remotion-dev/skills 설치** | 영상 PD, 개선 담당 | `npx skills add remotion-dev/skills`. 타이밍(`Easing.bezier(0.16,1,0.3,1)`, 0.3*fps 페이드), TransitionSeries 길이 공식(전체 = 장면 합 − 전환 합, `premountFor={fps}`), rough-notation 강조를 Claude가 맞게 쓴다 | 리모션 API를 잘못 쓰는 실수가 준다 | 0원 | 기존 PenMark·Wipe와 겹친다 → 새 부품은 기존 토큰을 따른다 | 펜 강조·전환은 **이미 함**(PenMark·Wipe). skills 설치는 **새로움** |
| 10 | **롱폼 앞쪽은 더 촘촘하게, 뒤로 갈수록 넓게** | 영상 PD | 첫 60초는 시각 변화 간격 ≤ 3~4초(HookNumber, Beat maxGap 3), 그 뒤는 지금처럼 6초 | 첫 1분 유지. 출처는 '인트로 10~20초마다 리셋, 이후 25~40초'(확인 안 함). 우리 6초 기준이 이미 더 촘촘하다 | 낮음(beatCues의 maxGap 인자만 바꾸면 된다) | 과하면 정신없다 → motioncheck로 재기 | **대부분 이미 함**(beatCues 6초, motioncheck 정지 15초). 앞쪽 3초는 새로움 |

이미 하고 있어서 상위 10에서 뺀 것:
- 차트 막대를 차례로 자라게 하기, 숫자 카운트업, 범주별 고정 색(charts.tsx, fm.tsx T 토큰)
- 썸네일 320×180 축소 확인(RULES 썸네일 관문 2)
- 문장 끝 잡음과 쉿소리 관문(clickscan·deess)
- 모방 금지와 템플릿 반복 회피(RULES '경쟁은 참고', beats seed)
- AI 합성 표시(RULES §4)

---

## 시제품 (work/video/src/motion-proto — 코디네이터 지시로 motion/ 대신 여기)
| 파일 | 무엇 | 쓰는 법 |
|---|---|---|
| `captionTiming.ts` | 순수 함수. `wordTimings(text, frames)`는 문장 오디오 길이를 어절의 '읽는 음절 수'(숫자 한 자리 1.5, % 3)로 나눠 단어 시각을 어림한다. `paginate(words, maxChars)`는 자막을 쪽으로 나누고, `activeWord`·`pageOf`는 지금 읽는 단어와 쪽을 찾는다 | 단어 시각(위스퍼 등)이 생기면 `wordTimings` 대신 실제 시각을 넣는다 |
| `numberSpeech.ts` | 순수 함수. `speakWon(324567000)`은 `{say:'약 3억 2천만 원', show:'3억 2,456만 7,000원', rounded:true}`를 돌려준다. `speakPct(41.4)`는 `약 41%` / `41.4%`. `numbersInSentence(s)`는 한 문장에 든 숫자 개수를 센다 | 대본을 쓸 때 say를 문장에 넣고, show는 화면에 넣는다 |
| `YtqParts.tsx` | `KaraokeCaption {s, dark?, maxChars?, speechFrac?, bottom?, size?}`는 `Caption {s}` 자리에 그대로 넣는다. `SayExact {n: SpokenNumber, label, source?, start?, x?, y?, size?}`는 큰 반올림 숫자 아래에 '정확히 …' 꼬리표를 띄운다 | `import {KaraokeCaption, SayExact} from './motion-proto/YtqParts'`, `import {speakWon} from './motion-proto/numberSpeech'` → `<SayExact n={speakWon(324567000)} label="상위 10% 문턱" source="통계청 가계금융복지조사" />` |

- 색은 fm.T 토큰만 썼다. 단어 강조는 밝기(0.45 → 1)와 크기(1.06배)로 하고, 주황은 쓰지 않았다(주황은 손그림 동그라미·파이어맵 숫자 전용 규칙).
- 시험
  - `node --test work/video/tests/yt_quality_proto.test.mjs`: 7개 통과
  - `py -3.12 -m pytest work/tests/test_yt_quality_video.py`: 2개 통과(node 22.6 미만이면 건너뜀)
  - 타입 검사: 스크래치 폴더에 remotion 4.0.532, react 19, typescript 5를 깔고 `tsc --strict`로 fm.tsx와 함께 통과
- 확인 안 함
  - 실제 렌더(work/video에 package.json·index.ts·Weekly.tsx가 저장소에 없어 번들을 못 돌렸다)
  - 단어 시각 어림과 실제 음성의 오차

---

## 분야별 출처표
표기: **원문 봄** = 본문을 직접 읽음. **검색 요약만 봄** = 웹 검색 결과 요약만 봄(본문 못 봄). **제목만 봄** = 검색 목록의 제목만 봄. 조회수는 전부 확인 안 함(이유는 '먼저 밝혀 둘 한계').

### 1) 대본 (사람 말투·첫 30초 훅)
| 출처 | 날짜 | 본 범위 | 바로 따라 할 방법 | 우리 |
|---|---|---|---|---|
| [prepublish.ai — First 30 Seconds: 3-Phase Opening](https://prepublish.ai/guides/first-30-seconds) | 확인 안 함 | 검색 요약만 봄 | 패턴 깨기 → 보상 약속 → 끝까지 볼 이유 | 일부 이미 함(E-2 훅) |
| [outlierkit — YouTube Script Writing 2026](https://outlierkit.com/resources/youtube-script-writing/) / [teleprompter.com — Retention Guide 2026](https://www.teleprompter.com/blog/youtube-audience-retention) | 확인 안 함 | 검색 요약만 봄 | 15초 안에 구체적 가치 문장(주장 52% vs 44%). 문장 길이 분산이 크면 유지율 1.8배(주장). 어느 글의 숫자인지는 확인 안 함 | 새로움(15초 검사). 분산은 ①에서 진행 중 |
| [junetapa — ChatGPT 유튜브 롱폼 대본 작성법 7가지 (2026)](https://junetapa.com/blog/dev/posts/ai-tools/chatgpt-%EC%9C%A0%ED%8A%9C%EB%B8%8C-%EB%8C%80%EB%B3%B8-%EC%9E%91%EC%84%B1%EB%B2%95.html) | 2026(월 확인 안 함) | 검색 요약만 봄 | "첫째로·둘째로", "~에 대해 알아보겠습니다" 같은 AI 패턴을 지운다. 내가 쓴 대본을 먼저 분석시키고 "이 스타일로"라고 시킨다 | 이미 함(aitell 사전, 대본 심사) |
| [prepublish.ai — Retention Benchmarks 2026](https://prepublish.ai/blog/youtube-retention-benchmarks-2026) | 확인 안 함 | 검색 요약만 봄 | 첫 1분 유지 65% 이상이면 평균 시청 시간 +58%(주장) | 판정 지표로만(분석 권한 생기면) |
| 내부: speechcompare.py | 2026-10-03 | 원문 봄 | 숫자 밀도 187 vs 52 | → 상위 10의 1번 |

### 2) 목소리 (TTS 자연스러움·한결같음)
| 출처 | 날짜 | 본 범위 | 바로 따라 할 방법 | 우리 |
|---|---|---|---|---|
| [Google Cloud — Gemini TTS prompting guide](https://docs.cloud.google.com/gemini-enterprise-agent-platform/models/text-to-speech/prompting-guide) / [ainarrator — Gemini TTS Best Practices](https://ainarrator.stackseekers.com/blog/gemini-tts-best-practices) | 확인 안 함 | 검색 요약만 봄 | voice design으로 목소리를 정해 두고 ID를 재사용한다. 긴 Audio Profile·Director's Notes는 목소리가 흔들리는 가장 큰 원인이다. "목소리 유지하라" 같은 지시는 넣지 않는다. 순간 소리는 `<short pause>`·`<breath>` 태그로 넣는다 | 짧은 지시는 이미 함. 참조 음성 고정은 새로움 |
| [Gemini 3.8 Flash TTS 모델 문서](https://ai.google.dev/gemini-api/docs/models/gemini-3.8-flash-tts) | 확인 안 함 | 제목만 봄 | — (긴 내레이션에서도 목소리가 일정하다는 주장은 요약에서 봄) | 쓰고 있음 |
| [캐럿 — 일레븐랩스 사용법 2026](https://carat.im/blog/elevenlabs-usage-guide) | 2026(월 확인 안 함) | 검색 요약만 봄 | Stability 75%, Similarity 85%. 숫자는 한글로 풀어 입력("이십오만 원"). 쉼표·마침표로 호흡 | 숫자 한글 풀기는 새로움. 일레븐랩스는 유료라 안 씀 |
| [gofaceless — AI Voiceover for YouTube (2026)](https://www.gofaceless.ai/en/blog/ai-voiceover-for-youtube) / [ElevenLabs blog](https://elevenlabs.io/blog/the-5-best-ai-voices-for-youtube-automation-and-faceless-videos) | 확인 안 함 | 검색 요약만 봄 | 완벽한 목소리보다 한결같은 목소리가 먼저. 말하듯 짧은 문장. TTS에 넣기 전에 소리 내 읽어 본다 | 이미 함(Charon 고정) |
| [remotion-dev/skills — remotion-markup/voiceover.md](https://github.com/remotion-dev/skills) | 커밋 날짜 확인 안 함 | 원문 봄 | 오디오 길이를 재서 `calculateMetadata`로 장면 길이를 정한다(초 × FPS 합). 전환이 있으면 겹친 만큼 뺀다 | 이미 함(규칙 '장면 길이를 목소리에 맞춘다'). 코드 관문은 ②에서 진행 중 |

### 3) 화면 (코드 모션그래픽·Remotion·차트·자막)
| 출처 | 날짜 | 본 범위 | 바로 따라 할 방법 | 우리 |
|---|---|---|---|---|
| [remotion-dev/skills](https://github.com/remotion-dev/skills)(GitHub 별 4.8k) | 커밋 날짜 확인 안 함 | 원문 봄 | `npx skills add remotion-dev/skills`. timing.md: `interpolate(frame,[0,0.3*fps],[0,1],{easing: Easing.bezier(0.16,1,0.3,1), clamp})`, 스프링 `damping:200`. transitions.md: `premountFor={fps}`, 전체 = 장면 합 − 전환 합, 전환 15~25프레임. text-highlights.md: `@remotion/rough-notation`의 Highlight·Circle·Underline에 `progress=interpolate(...)`. silence-detection.md: `loudnorm=print_format=json`으로 잰 뒤 `silencedetect=noise=<input_thresh>dB:d=0.5`, 0.2초 미만 틈은 합친다 | 강조·전환은 이미 함. skills 설치·무음 자동 자르기는 새로움 |
| [remotion-dev/skills — remotion-captions/display-captions.md](https://github.com/remotion-dev/skills) | 확인 안 함 | 원문 봄 | `@remotion/captions` Caption은 `{text,startMs,endMs,timestampMs,confidence}`이고 text 앞에 공백을 둔다. 1920 화면에서 자막 폭 900, 아래 120px | 단어 강조는 시제품 |
| Remotion `createTikTokStyleCaptions()`·Word Highlight Captions([display 문서](https://www.remotion.dev/docs/captions/displaying)) | 확인 안 함 | 검색 요약만 봄 | `combineTokensWithinMilliseconds`로 한 쪽 단어 수를 조절하고, token의 fromMs·toMs로 지금 단어를 강조 | 시제품 `KaraokeCaption`이 같은 구조(단어 시각은 어림) |
| ["Claude Code Can Now Automate Your Videos (Remotion + Opus 5.5)"](https://www.youtube.com/watch?v=6_rCyryA6hg) | 2026-10-01(검색 요약) | 제목만 봄 | — | — |
| ["클로드 코드 X remotion 미친 조합! (비개발자 가이드)"](https://www.youtube.com/watch?v=uQPegX8CiyA) · ["이제 편집조차 필요 없습니다"](https://www.youtube.com/watch?v=I9Ib9au7js4) · ["클로드 코드로 유튜브 영상을 자동화할 수 있다고?"](https://www.youtube.com/watch?v=UM9FmXJQ3yg) | 확인 안 함 | 제목만 봄 | — | — |
| [Threads @seize.more — 클로드코드로 유튜브 쇼츠](https://www.threads.com/@seize.more/post/DWBXH9uEiU_) | 확인 안 함 | 검색 요약만 봄 | 씬 템플릿을 React로 만들어 두고, JSON 하나와 명령 한 줄로 목소리(edge-tts)·자막까지 만든다 | 이미 함(props json → Remotion). 다만 '주제만 바꿔 찍어내기'는 템플릿 반복 정책 위험 |
| [kpistudio — Animated Bar Chart for YouTube](https://kpistudio.app/guides/bar-chart-for-youtube-video) / [alienart — bar chart race](https://alienart.io/visualizations/bar-chart-race) | 확인 안 함 | 검색 요약만 봄 | 막대는 한 화면에 10~15개 이하, 범주마다 고정 색, 날짜 카운터를 크게, 막대는 차례로 자라게 | 이미 함(BarSeries 차례 자라기, 토큰 색) |

### 4) 썸네일 (클릭률)
| 출처 | 날짜 | 본 범위 | 바로 따라 할 방법 | 우리 |
|---|---|---|---|---|
| [vidIQ — Test & Compare](https://vidiq.com/blog/post/youtube-launches-new-thumbnail-testing-tool/) / [ppc.land — 제목까지 A/B 확대](https://ppc.land/youtube-expands-a-b-testing-to-include-titles-alongside-thumbnails/) / [outlierkit — 3 Variants Guide 2026](https://outlierkit.com/resources/youtube-ab-testing-3-variants-guide-2026/) | 2025-12 확대(검색 요약) | 검색 요약만 봄 | 제목, 썸네일, 제목+썸네일 중 하나로 3안까지. 승자는 '노출당 시청 시간'. 며칠에서 2주. 결과는 Winner·Performed Same·Inconclusive | **새로움** |
| [yt-seo-architect — AI Thumbnail & Title A/B 2026](https://yt-seo-architect.vercel.app/blog/youtube-thumbnail-ab-testing-guide) / [miraflow — CTR 2026](https://miraflow.ai/blog/youtube-ctr-2026-good-click-through-rate-ai-thumbnails) | 확인 안 함 | 검색 요약만 봄 | AI로 5~10안을 만들고 대비·글자 가독성·호기심으로 점수를 매겨 상위 3안을 Test & Compare에 건다. 글자는 5단어 이하. 시청의 70%가 모바일 | 5단어·모바일은 이미 함(숫자 1개 + 말 1개, 320×180). 5~10안 점수 매기기는 새로움 |
| [lovart — YouTube 썸네일 디자인 2026](https://www.lovart.ai/ko/blog/youtube-thumbnail-design-science-2027) | 확인 안 함 | 검색 요약만 봄 | 과장 표정형은 줄고 다큐형이 는다. 보색 대비, 3~6단어, 핵심 요소 3개 이하 | 이미 함(캐릭터 없이 숫자·글자) |
| [메일리 visionmkt — 클릭률 극한으로](https://maily.so/visionmkt.lucas/posts/wjzd3nqyr3p) | 확인 안 함 | 제목만 봄 | — | — |

### 5) 편집 리듬 (컷 길이·장면 전환)
| 출처 | 날짜 | 본 범위 | 바로 따라 할 방법 | 우리 |
|---|---|---|---|---|
| [increditors — Video Pacing for Retention](https://increditors.com/video-pacing-youtube-retention-science/) / [air.io — Advanced retention editing](https://air.io/en/youtube-hacks/advanced-retention-editing-cutting-patterns-that-keep-viewers-past-minute-8) | 확인 안 함 | 검색 요약만 봄 | 롱폼 인트로는 10~20초마다 시각 리셋, 이후 25~40초. 설명 구간은 10~15초 빠른 컷, 예시는 40초까지 머문다. 경험칙은 5~7초마다 무언가를 바꾸는 것 | 이미 더 촘촘함(Beat 6초, 정지 15초 관문) |
| [OpusClip — Ideal Shorts Length & Format](https://www.opus.pro/blog/ideal-youtube-shorts-length-format-retention) | 확인 안 함 | 검색 요약만 봄 | 쇼츠는 2~4초마다 컷·각도·요소 변화 | 쇼츠 카드는 새로움(상위 10의 3번) |
| remotion-dev/skills transitions.md | 확인 안 함 | 원문 봄 | 전환은 linearTiming 20프레임 또는 springTiming 25프레임. fade·slide·wipe·flip·clockWipe | 이미 함(Wipe 12프레임, seed로 방향) |
| 내부: motioncheck.py 경쟁 실측 | 2026-10-02 | 원문 봄 | 매경은 움직임 88%·최장 정지 6.0초, 수페TV는 12%·23.8초 | 기준 |

### 6) 쇼츠 첫 1초
| 출처 | 날짜 | 본 범위 | 바로 따라 할 방법 | 우리 |
|---|---|---|---|---|
| [reelforge — Shorts Algorithm 2026](https://reelforgeai.io/blog/youtube-shorts-algorithm-2026-complete-guide) / [blitzcut — Shorts Algorithm 2026](https://blitzcutai.com/blog/youtube-shorts-algorithm-2026) | 확인 안 함 | 검색 요약만 봄 | 1초 유지가 가장 큰 신호(주장). 첫 2초를 넘기면 끝까지 볼 확률이 약 60% 오른다(주장) | 첫 1초 그림은 이미 함 |
| [aibrify — Shorts Retention Curve Playbook](https://aibrify.com/blog/youtube-shorts-retention-curve-playbook) / [tubeanalytics — Shorts Retention Guide](https://www.tubeanalytics.net/blog/youtube-shorts-retention-guide) | 확인 안 함 | 검색 요약만 봄 | 첫 3초 80% 이상, 중간 60% 이상, 평균 시청 비율 70% 이상. 스와이프 이탈은 10~30%가 정상이고 40%를 넘으면 경고 | 판정 기준 후보(새로움, 쇼츠 분석 지표로 쓰기) |
| [fragilegfx — Static vs Animated Overlays 2026](https://fragilegfx.com/blogs/news/static-vs-animated-overlays-which-performs-better-for-growth-in-2026) / [adshortsai — Shorts from photos](https://adshortsai.com/en/youtube-shorts-from-photos/) | 확인 안 함 | 검색 요약만 봄 | 0.8초 안에 굵은 글자를 띄운다. 사진 슬라이드는 '아무 일도 안 일어나서' 스와이프당한다. 한 장에 오래 머물지 않는다 | **새로움**(7초 정지 카드에 미세 움직임 넣기) |
| [viralpulse — 쇼츠 첫 3초가 전부다](https://viralpulse.net/blog/shorts-first-3-seconds-hook-strategy) / [라이크셀러 — 피드 이탈 줄이기](https://likeseller.co.kr/article/%EB%B8%94%EB%A1%9C%EA%B7%B8/8/882/) | 확인 안 함 | 검색 요약만 봄 | 결과를 먼저 보여 준다(Result-First). 동작 중간에서 시작한다(Mid-Action) | 이미 함(표 한 장 결과 먼저) |

### 정책 (모든 분야에 걸림)
| 출처 | 날짜 | 본 범위 | 요점 | 우리 |
|---|---|---|---|---|
| [lenspov — 2026 Inauthentic-Content Policy](https://lenspov.com/articles/youtube-ai-content-demonetization-2026) / [ytzolo — Repetitive Content & AI Slop 2026](https://ytzolo.com/blog/youtube-repetitive-content-policy-ai-slop-2026/) | 이름 변경 날짜가 요약에서 2026-07-15로 나왔지만 확인 안 함 | 검색 요약만 봄 | 템플릿으로 대량 생산한 AI 콘텐츠는 수익화 제외. 해설·분석·편집 같은 사람의 창작이 있으면 수익화 유지 | 이미 함(RULES §5, '터진 형식' 규칙, beats seed) |

---

## 확인 안 함 (모음)
- 모든 영상의 조회수·참여 순위, 그리고 영상 본문(자막·타임스탬프). youtube.com 차단, vidIQ 크레딧 0.
- 검색 요약에 나온 숫자 전부(52% vs 44%, 1.8배, CTR 15~40%, 1초 유지 신호, 0.8초 등). 출처 글 본문을 못 봤다.
- Test & Compare를 우리 채널에서 쓸 자격이 있는지, API로 걸 수 있는지.
- Gemini TTS 참조 음성(voice design)을 무료 등급에서 쓸 수 있는지.
- 시제품의 실제 렌더 결과, 단어 시각 어림의 오차.
