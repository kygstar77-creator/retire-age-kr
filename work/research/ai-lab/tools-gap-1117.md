# AI 도구 점검 5판 — 2026-11-17 03시 (벤치마크 루프 대상 5)

1111 약속대로 **목소리(TTS)를 이미지보다 먼저** 돌렸다. 그 대가로 이미지(apt·bank)는 다시 익명 한도에 막혔다.

## ① 지난 개선(1111) 반영 — 4/5 (일부 1)
| 개선점(1111) | 상태 | 근거 |
|---|---|---|
| 사람 뒷모습 장면 RealVisXL vs MiniMax-H3 두 판 비교(video-producer) | 일부 | archive/today-2026-11-14.md:87 PD 11/12 06:18 — H-4·N-3에 AI 사람 장면 없음(전부 Pexels) → 'AI 사람 장면이 처음 들어가는 편에서'로 미룸. 미룬 이유 사실과 맞음 |
| AI 티 G1~G3 editor 점검표 | 반영 | editor/style-guide.md:223~226 |
| HF 무료 계정 결재 approvals.md | 반영(올림) · **결정 안 남** | approvals.md:191 '상태: 요청' 그대로(6일) |
| gemini-2.5-flash-preview-tts(11/17 종료) 후보 목록에서 빼기 | 반영 | longform/ep/A-1/voice.py:10·sonpum2/tour_voice.py:10 목록에 없음(남은 곳은 .claude/worktrees 옛 사본뿐) |
| ZONOS3 TTS를 다음 회차 먼저 | 반영 | 이번 ③ |

## ② 새 도구(11/11~11/17) — HF API 원문(11/17 03시 열람)
| 도구 | 날짜 | 라이선스 | 우리 조건 | 판정 |
|---|---|---|---|---|
| ZONOS3-Mini(Zyphra) | 11/9 | Apache-2.0 | 한국어(ko) 목소리 Minjun·Seoyeon. 공식 Space는 API 꺼짐, mrfakename/zonos3-mini로 됨(1줄 6~8초 GPU) | **시험함 ③** |
| akhaliq/minimax-h3-image-pdmd-2step | 11/10 | 어댑터 Apache-2.0, 바탕 H3 커뮤니티 라이선스 | 2단계 증류 → 한 장 GPU 시간이 짧아 익명 한도 안 장 수가 늘 가능성. 통합본 40GB·ComfyUI LoRA 1.96GB | 시험 못 함(한도) |
| Abiray/MiniMax-H3-Image-GGUF | 11/10 | H3 커뮤니티 라이선스 | 가장 작은 Q2_K 6.9GB(+글 인코더 별도) — 6GB VRAM·빈 RAM 1~3GB라 로컬 실행 **확인 안 함** | 보류 |
| Pika-Labs/Pika-H3-Flex(그림→영상) | 10/29 | H3 커뮤니티 라이선스 | 지금 push/pan 대신 정지 그림을 실제로 움직일 후보. Space 있음(zero GPU) | 시험 못 함(한도) |
| Comfy-Org/PAN2(글→영상) | 11/15 | Apache-2.0 | Space 없음, ComfyUI 전용 | 보류 |
| n4ze3m/tiny-voca·owensong/Inflect-Mini-v3 | 11/10~14 | Apache-2.0 | 영어만 | 제외 |
| Oomni/mithi-v1-flash | 11/7 | Apache-2.0 | 인도 말만 | 제외 |
| ConwayResearch/Underdog-Woof | 11/5 | 비상업 | — | 제외 |
- 구글 쪽: Gemini API 변경 기록·Cloud TTS 출시 노트에 11월 새 줄 못 찾음(검색 11/17). Chirp 3 HD 그대로.

## ③ 목소리 — Chirp 3 HD Charon(지금) vs ZONOS3-Mini Minjun(새)
대본: H-4 say_v2.txt 4줄 '답부터 말하면… 18번째였습니다. 중간보다 아래예요.' + 2줄 질문. 파일은 scratchpad(커밋 안 함).
판정: 제미나이 3-flash가 이름 가린 채 듣고 1~10점, 순서를 바꿔 다시.

| 판(순서) | Chirp | ZONOS 기본 | ZONOS Calm |
|---|---|---|---|
| 4줄 1차 (Chirp=[pause] 태그판) | 7 | 8 | 9 |
| 4줄 순서 바꿈 ([pause] 태그판) | **9** | 7 | 4 |
| 4줄 공정판 (Chirp=지금 파이프라인 pause_v 2, 태그 없음) | 8 | **9** | 4 |
| 2줄 질문 | **9** | 8 | — |
| 2줄 질문 순서 바꿈 | **10** | 8 | — |
| 길이(4줄) | 7.5초 | 9.1초(+22%) | 8.5초 |
- 판정: **Chirp 유지.** 1등 Chirp 3/5·ZONOS 2/5로 판정기가 순서에 따라 뒤집힘(같은 Calm 파일이 9점↔4점). ZONOS는 같은 줄이 22% 느려 우리 말 속도(1.1배) 맞추려면 rate 손봐야 하고, 한도 걸리는 Space에 기대야 한다. 바꿀 근거 없음. 공식 지원 한국어 목소리 2개뿐.
- 두 판정기 모두 '18번째'를 '십팔/열여덟'으로 서로 다르게 받아씀 → 숫자 읽기 차이는 이 방법으로 가를 수 없다(**확인 안 함**).

### 새로 찾은 것: Chirp가 [pause] 태그 자리에 '음'을 넣는다
같은 문장을 쉼 태그만 바꿔 받고 제미나이에 '추임새까지 소리 그대로' 받아쓰게 함:
| 태그(줄 안 문장 끝) | 받아쓰기 |
|---|---|
| `[pause]` (cloudtts.py markup 기본값) 2개 파일 | '…번째였습니다 **음** 중간보다 아래예요' 2/2 |
| `[pause short]` | 추임새 없음 |
| 태그 없음(pause_v 2, 지금 롱폼) | 추임새 없음 |
- 이름 가린 판정에서도 [pause]판에만 '대본에 없는 음이 들어감'이 2/2 지적됨.
- 지금 업로드 경로는 안전: H-4·H-5·JT-1·N-3·K-1 tts.json 전부 pause_v 2(줄 안 태그 없음), voice.json에 `[pause]` 0개·`[pause short]`만. 쇼츠는 롱폼 wav 재사용(n3fclip.py:3).
- 위험 남은 곳: cloudtts.py `say` 명령과 `markup()` 기본값이 아직 `[pause]`. pause_v 2 이전(10/19 전) 편은 이 태그로 녹음됨 — 올라간 옛 편에 '음'이 있는지는 **확인 안 함**.
- 표본: 한 문장·한 목소리 2파일. 넓히기 전엔 '이 문장에서 2/2'로만 쓴다.

## ④ 실사 장면 — 이번에도 apt·bank 못 봄
MiniMaxAI/MiniMax-H3-Image Space 두 번 다 "exceeded your ZeroGPU runs limit"(TTS 5번 뒤). 1105·1111·1117 세 번 연속 3장면 중 1장면 이하. 결정(H3를 아파트·서류 장면에 쓰나)은 계정 없이는 못 낸다 → 기준선 RealVisXL V5 유지, 교체 지시 없음.

## ⑤ 성과 — 판단 못 함(같은 이유)
ytanalytics recent 30(11/17 03시): H-3 gvlX2KQcI8g(AI 실사 5장면) 조회 602→**611**, 평균 시청 비율 12.11→**12.00%**. 같은 표 롱폼 scV67BQvC4Q 43.6%·mkAxQPGaDqc 36.7%·SGx7UD-6RNE 26.2%·_fTgGr0dR0I 16.4%·NNcjTE0L7yg 13.9%보다 낮음. AI 장면 탓인지 곡선 구간은 안 봄(**확인 안 함**).

## ⑥ AI 티 — editor 점검표 V1로 넣음
- V1 목소리 추임새: 대본에 없는 '음·어'가 녹음에 들어감(Chirp `[pause]` 태그 자리, 위 표). 녹음 받아쓰기에서 대본에 없는 한 글자 추임새가 나오면 그 줄 다시 받기.

## 결정 필요(사장님)
- HF 무료 계정 가입(11/11 요청, 6일째 대기). 돈 0원. 없으면 새 영상 도구 비교가 매번 3장면 중 1장면에서 멈춤(3회 연속).

## 출처
huggingface.co/api/models?pipeline_tag=text-to-image·text-to-video·text-to-speech·image-to-video&sort=trendingScore(11/17) · api/models/Zyphra/ZONOS3-Mini·akhaliq/minimax-h3-image-pdmd-2step·Abiray/MiniMax-H3-Image-GGUF(tree)·Pika-Labs/Pika-H3-Flex·Comfy-Org/PAN2 · ai.google.dev/gemini-api/docs/changelog · docs.cloud.google.com/text-to-speech/docs/release-notes
