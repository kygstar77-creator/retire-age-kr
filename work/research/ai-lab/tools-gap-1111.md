# AI 도구 점검 4판 — 2026-11-11 03시 (벤치마크 루프 대상 5)

11/11 쉼 풂(today.md 11/10 21:43 회의) 뒤 첫 회차. 무거운 렌더는 5초 1개만 돌렸다.

## ① 지난 개선(1105) 반영 — 0/4
| 개선점(1105) | 상태 | 근거 |
|---|---|---|
| Klein 다시 시험('Korean license plates·blank paper, no printed text' 덧붙여) | 안 됨 | ai-footage-1019/_pub에 klein 파일 3개뿐(11/5 것). 담당이 정해지지 않았다(1105는 지시 0건) |
| AI 티 G1(외국 번호판)·G2(서류에 영어 제목) → editor 점검표 | 안 됨 | editor/style-guide.md에 '번호판' 0건 → 이번 회차에 G1~G3 넣음 |
| 결재 3건(HF 무료 계정·Ming 가중치·Omni Flash) approvals에 올리기 | 안 됨 | approvals.md에 'HF'·'Ming' 0건, Omni Flash는 10/12 줄(Veo Lite 경로 살아 있던 때)만 있음 → 이번에 올림 |
| gemini-2.5-flash-preview-tts 11/17 종료 대비 | 안 됨 | research/sonpum2/tour_voice.py:10, **ep/A-1/voice.py:10**(1105에서 놓친 곳)의 후보 목록에 그대로 있음. 둘 다 앞 순번 모델이 먼저라 지금 업로드 경로는 안 깨짐 |

## ② 새 도구(10/12~11/11) — HF API·모델 카드 원문(11/11 열람)
| 도구 | 날짜 | 라이선스(원문) | 우리 조건 | 판정 |
|---|---|---|---|---|
| **MiniMax-H3-Image**(MiniMaxAI) | 11/3 | 커뮤니티 라이선스. 연매출 $1M 넘거나 남에게 생성 서비스 제공하면 별도 허가(IV.1). 상업 제품 UI에 'MiniMax-H3-Image' 표시(IV.2). 공개 게시물은 기계 생성임을 분명히 밝혀야 함(Exhibit A.12) | 33.1B·DiT 66GB → 로컬 불가. HF Space zero-a10g 익명 1장 24초 | **시험함** |
| **MOSS-Image**(OpenMOSS, Base·SFT) | 10/11 | Apache-2.0 | 5B. negative prompt 칸 있음(Klein 약점 G2 해결 가능). Space 익명 1장 GPU 49초 | **시험함** |
| ZONOS3-Mini(Zyphra) TTS | 11/9 | Apache-2.0 | 한국어 정규화·기본 목소리 Minjun(남)·Seoyeon(여). 100M 활성, 브라우저 WebGPU·CUDA 서버로 로컬 가능 | 시험 **막힘**(아래) |
| drama-3(fishaudio) TTS | 10/1 | fish-audio-research-license | 이름대로 연구용 → 상업 사용 확인 전 탈락 | 제외 |
| Qwen-Image-2.1-Turbo | 10/9 | Qwen Research License(상업 금지, 1105와 같음) | — | 제외 |

## ③ 실사 기준 장면 'couple' — 같은 프롬프트·같은 NEG(tools/localgen/sdxl_gen.py)
파일(커밋 안 함): strategy/ai-footage-1019/_pub/couple__minimax-h3-hfspace.png·couple__moss-image-hfspace-portrait.png, clips/couple__minimax-h3-hfspace.mp4(render.sh push 5초).
apt·bank는 **확인 안 함**: H3 1장 뒤 "You have exceeded your ZeroGPU runs limit"(익명 하루 한도, MOSS 49초+H3 24초).

| 볼 것 | RealVisXL V5(지금) | FLUX 3 Klein(1105) | MiniMax-H3(새) | MOSS-Image(새) |
|---|---|---|---|---|
| 두 사람 | 체형 같아 '두 노인' | 남녀 분명 | 남녀 분명, **손을 잡음**(손가락 정상, 겹침 없음) | 여자 뽀글 파마·빨간 단화 → 가장 '한국 동네 어르신' |
| 손·발 | 정상 | 정상 | 정상. 여자 왼손 가방이 둥근 모자처럼 생김(뜻이 애매) | 정상 |
| 한국다움 | 기와 처마·안개(관광지 느낌) | 낙엽 길, 배경 약함 | 왼쪽 상가 차양·초록 간판 흐림(글자 안 읽힘), 가로수 길 | 초록 철제 울타리·버스·횡단보도 |
| 광택·색 | 안개로 탁함 | 단풍 채도 높음, 길에 검은 얼룩 | 필름 톤, 과한 광택 없음 | 필름 입자, 가장 덜 AI 같음 |
| 움직임(4.9초 끝) | 뭉개짐 없음 | 뭉개짐 없음 | 뭉개짐 없음 | (세로라 렌더 안 함) |
| 문제 | — | — | 라이선스 표시 2가지 | **내가 폭·높이를 바꿔 넣어 768×1344 세로로 나옴**(in_3=높이) — 가로는 확인 안 함 |

- 판정: couple 한 장면에서는 **H3 > Klein > RealVisXL**. MOSS는 한국다움이 가장 좋지만 세로라 가로 장면으로는 못 견줌 — 대신 **쇼츠(9:16) 배경 후보**로 바로 쓸 수 있는 크기다.
- 교체 지시는 하지 않는다: 3장면 중 1장면만 봤고(1105 Klein도 couple만 나았다가 apt·bank에서 졌다), H3는 라이선스 조건이 붙는다. 대신 **사람 뒷모습 장면은 두 판을 만들어 눈으로 고르라**는 지시를 건다(today.md).
- H3를 쓰면 붙는 일: 설명란에 'AI 생성 장면 일부: MiniMax-H3-Image' 한 줄 + 업로드 containsSyntheticMedia 켜기(이미 규칙). 우리 연매출 $1M 미만, 남에게 생성 서비스 안 함 → 별도 허가 불필요(IV.1 원문 기준).

## ④ 성과 — 판단 못 함(1105와 같음)
ytanalytics recent 30(11/11 03시): H-3 gvlX2KQcI8g(AI 실사 5장면) 조회 585→**602**, 평균 시청 비율 12.87→**12.11%**. 같은 표 롱폼 mkAxQPGaDqc 35.8%·G1oI47miUuo 26.8%보다 여전히 가장 낮다. AI 장면 효과인지 주제·길이 탓인지는 곡선 구간을 안 봐서 **확인 안 함**.

## ⑤ 목소리 — ZONOS3-Mini 확인 안 함
Space 3곳(mrfakename·fffiloni·fishaudio) 모두 zero-a10g라 이미지 2장 뒤 같은 익명 한도에 걸린다. 1105 Ming도 같은 이유로 막혔다. **다음 대상 5 회차는 TTS를 이미지보다 먼저** 돌린다(H-4 대본 숫자 줄 1개, Minjun vs Chirp Charon). 로컬 CUDA 서버(6GB에서 100M 활성)는 설치가 커서 이번엔 안 함.

## ⑥ AI 티(그림) — editor 점검표 G1~G3로 넣음
- G1 차 번호판·앰블럼이 외국 것(1105 Klein 아파트). 차 보이는 장면은 확대.
- G2 negative 칸 없는 모델은 서류에 영어 제목을 또렷하게 그림(1105 Klein 은행).
- G3 손에 든 물건이 무엇인지 안 읽힘(H3 couple 여자 가방=둥근 모자 모양). 손에 든 물건은 확대해서 이름을 댈 수 있어야 통과.

## 결재(approvals.md에 올림)
- HF 무료 계정 가입: ZeroGPU 하루 익명 약 2분 → 계정 5분(1105 근거). 이번에도 3장면 중 1장면에서 멈춤. 돈 0원, 가입만.

## 출처
huggingface.co/api/models/MiniMaxAI/MiniMax-H3-Image·README·LICENSE(IV·Exhibit A) · huggingface.co/OpenMOSS-Team/MOSS-Image-SFT·Base(apache-2.0) · huggingface.co/Zyphra/ZONOS3-Mini README · huggingface.co/api/models/fishaudio/drama-3 · HF trending text-to-image·text-to-speech(11/11 03시)
