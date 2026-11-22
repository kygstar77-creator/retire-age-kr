# AI 도구 점검 6판 — 2026-11-23 03시 (벤치마크 루프 대상 5)

## ① 지난 개선(1117) 반영 — 3/4
| 개선점(1117) | 상태 | 근거 |
|---|---|---|
| cloudtts.py `markup()`·`synth()`·`say` 쉼 태그 기본값 `[pause]`→없음(video-producer, 11/17 23:59) | 반영 | work/cloudtts.py:33 주석·sent_tag=None, today.md 11/17 06:22 완료 줄('음' 0/2) |
| editor 점검표 V1(대본에 없는 추임새) | 반영 | editor/style-guide.md:250~251 |
| 1111 이월: 사람 뒷모습 장면 RealVisXL vs H3 두 판(video-producer) | 해당 편 없음 | 11/17 뒤 편 D-ETF-1·H-6·KOSPI-1 meta.json synthetic_note 모두 'AI 생성 그림 없음(실사 Pexels)' — 조건(AI 사람 장면 들어가는 편)이 안 생김 |
| HF 무료 계정 결재 | **안 됨** | approvals.md:191 '상태: 요청' 12일째. 오늘 H3 apt·bank가 **4회 연속** "exceeded your ZeroGPU runs limit" |

바로잡음: 1117판 "Gemini API 변경 기록에 11월 새 줄 못 찾음"은 틀렸다. 같은 페이지에 11/4(3.8 Flash TTS 목소리 리믹스)·11/5(Omni 1.2 Flash GA)·11/10~12 줄이 있었다(11/23 다시 열람). 1105판이 11/4까지는 이미 적어 두었고, 우리 판단(Chirp 유지·Omni 유료)은 바뀌지 않는다.

## ② 새 도구(11/17~11/23) — HF API·구글 원문(11/23 03시 열람)
| 도구 | 날짜 | 라이선스 | 우리 조건 | 판정 |
|---|---|---|---|---|
| lvladikov/MOSS-SFT-Distill-4step-LoRA (+바탕 OpenMOSS MOSS-Image-SFT) | 11/19 | 둘 다 Apache-2.0 | 4스텝 증류. Space hugging-apps/moss-image-4step-lora, 1824×1024 가로 지원, 익명으로 장당 9~19초 | **시험함 ③** |
| KittenML/kitten-tts-2-mini | 11/13 | Apache-2.0 | 82M, CPU ONNX 82.7MB, 한국어 목소리 Seoyeon·Minjun·Jihoon. 이 PC에서 로컬로 돎(한 줄 2.6~3.6초 CPU) | **시험함 ④** |
| apple/FastFrames-L·S (글→영상) | 11/16 | apple-amlr — "exclusively for Research Purposes" | 상업 불가 | 제외 |
| kyutai/AURA-1.3B (그림→영상) | 11/18 | cc-by-nc-4.0 | 비상업 | 제외 |
| Comfy-Org/LongCat-Video-Avatar | 11/18 | MIT | 말하는 얼굴 아바타 — 우리는 얼굴 안 씀(1019 정책) | 제외 |
| H3-Tiny/MiniMax-H3-Tiny-ComfyUI · ReDiverse-MiniMax-H3 | 11/16~21 | other(H3 커뮤니티) | Space 있음(ReDiverse) 하지만 같은 ZeroGPU 한도 | 보류(HF 계정 뒤) |
| mehdi-hf/cilla-mini | 11/16 | cc-by-nc-4.0, 페르시아어 | — | 제외 |
| 구글: Gemini 3.5 Transcribe 음성 편집(11/17)·Gemini 4 Neon(11/18, 유료 등급)·Genie 4(11/19, 실시간 세계 생성) | — | — | 받아쓰기·대본엔 기존 무료 모델로 충분, Genie는 용도 밖 | 시험 안 함 |
- Cloud TTS 출시 노트: 11월 Chirp 3 HD 새 줄 못 찾음(검색 11/23). Chirp 3 HD Charon 그대로.

## ③ 실사 장면 — RealVisXL V5(지금) vs MOSS 4-step(새), 같은 프롬프트(sdxl_gen.py PROMPTS) + render.sh 5초
파일(커밋 안 함): strategy/ai-footage-1019/_pub/{apt,bank}__moss4step-hfspace.png, clips/bank__moss4step-hfspace.mp4(push).
H3 apt·bank는 MOSS 2장(약 28초) 뒤 익명 한도로 또 못 봄.

| 볼 것 | bank RealVisXL | bank MOSS 4-step | apt RealVisXL | apt MOSS 4-step |
|---|---|---|---|---|
| 손가락 | 정상 | 정상(엄지·검지로 펜, 왼손 손가락 4개 바닥에 평평) | — | — |
| 글자 깨짐 | 서류에 **바코드·뜻 없는 영어**, 다가가기 끝(4.9초)에 더 크게 보임 | 서류 줄이 흐린 회색 선, 오른쪽 끝 작은 가짜 글자 1곳 | 없음 | 없음 |
| 과한 광택·주름 | 주름 과함, 탁자 반질 | 주름 보통(50~60대), 탁자 무광 | 없음 | 없음 |
| 한국다움 | 중립 | 중립 | **5층 저층 아파트(물탱크·실외기)+고층 단지+산** | 흰 고층이지만 **발코니 없음·창 배치 불규칙** → 호텔·관공서처럼 보임 |
| 움직임(push 5초) | 서류 기호가 커짐 | 어색함 없음 | — | — |
| 시간 | 장당 141~153초(로컬) | 9초(Space) | 같음 | 19초 |

- 판정: **손·서류 장면은 MOSS 4-step이 낫다**(AI 티 '바코드 글자'가 사라짐). **아파트는 RealVisXL 유지**.
- 한계: 장면당 1장(seed 1)씩. 익명 한도 안에서만 돎 — 하루 장 수는 **확인 안 함**(H3가 이어서 막힌 걸 보면 MOSS 2장 뒤 남는 게 적다).

## ④ 목소리 — Chirp 3 HD Charon(지금) vs KittenTTS 2 Mini(로컬)
대본: H-4 say_v2.txt 4행(답 줄)·2행(질문 줄). Chirp는 cloudtts.py `say`(korsay 안 거침), Kitten은 같은 글 그대로. 이름 가리고 제미나이가 1~10점, 순서 바꿔 다시.

| 판정(모델·순서) | Chirp | Kitten Minjun | Kitten Jihoon |
|---|---|---|---|
| 답 줄, 3.5-flash, Chirp 먼저 | **9** | 6 | 5 |
| 답 줄, 3-flash, Chirp 마지막 | **9** | 4('비싼'→'비산') | 6 |
| 질문 줄, 3.5-flash, Chirp 먼저 | **10** | 6('84㎡'를 '84'로, 단위 빠짐) | — |
| 질문 줄, 3-flash, Chirp 뒤 | **10** | 3(84 잘못 읽음·㎡ 빠짐) | — |
| 길이(답 줄) | 8.2초 | 6.8초 | 6.9초 |
- 판정: **Chirp 유지.** 4/4 판정 모두 Chirp 1등, 차이 3~7점. Kitten은 단위(㎡)를 빠뜨리고 발음 틀림이 있다.
- 판정기가 3.5-flash 순서 바꿈·4-hydrogen에서 429·503(무료 한도) — 3-flash로 대신함.

### 새로 찾은 것: korsay를 안 거치면 Chirp도 '18번째'를 '십팔 번째'로 읽는다
- 3-flash 받아쓰기(답 줄): Chirp '…**십팔 번째**였습니다'. 1117판의 '십팔/열여덟 확인 안 함'은 이것이었다 — 그때도 `say`로 받았다.
- 업로드 경로는 안전: lfvoice.py:86~88이 Chirp 편에 korsay.say를 거침 → `korsay.say('18번째')`='열여덟 번째'(11/23 확인). 남는 위험은 korsay를 안 거치는 길(cloudtts `say` 명령, 시험·쇼츠 단독 녹음).
- 이 점검의 비교 방법도 고친다: 다음 TTS 비교부터는 **모든 후보에 korsay.say(…, 2) 결과를 넣는다**(지금 비교는 Chirp에 불리했는데도 이겼다).

## ⑤ 성과
ytanalytics recent 30(11/23 03시, 최근 30일 창): H-3 gvlX2KQcI8g(AI 실사 5장면) 조회 569·평균 시청 비율 **11.65%**(11/17 12.00%). 같은 창 롱폼 mkAxQPGaDqc 36.94%·scV67BQvC4Q 43.71%·MRQqitzEgDw 40.05%보다 여전히 낮음. 11/17 뒤 AI 장면 넣은 편이 없어 AI 장면 효과는 **판단 못 함**. 창이 30일로 움직여 조회 수는 지난 판과 바로 비교 못 함.

## ⑥ AI 티 — editor 점검표 V2로 넣음
- V2 숫자 서수 한자어 읽기: korsay를 안 거친 녹음은 '18번째'를 '십팔 번째'로 읽는다(Chirp, 11/23 받아쓰기). 받아쓰기에서 '십X 번째'·'X 번째'가 한자어로 나오면 korsay 거쳤는지 보고 다시 받기.

## 결정 필요(사장님)
- HF 무료 계정 가입(11/11 요청, 12일째). 돈 0원. 없으면 H3 apt·bank 비교가 4회 연속 멈춘다.

## 출처
huggingface.co/api/models?pipeline_tag=text-to-image·text-to-video·image-to-video·text-to-speech·automatic-speech-recognition&sort=trendingScore(11/23) · api/models/lvladikov/MOSS-SFT-Distill-4step-LoRA(README)·OpenMOSS-Team/MOSS-Image-SFT·KittenML/kitten-tts-2-mini(README)·apple/FastFrames-L(LICENSE)·kyutai/AURA-1.3B·Comfy-Org/LongCat-Video-Avatar · ai.google.dev/gemini-api/docs/changelog·pricing · cloud.google.com/text-to-speech/docs/release-notes
