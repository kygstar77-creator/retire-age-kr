# AI 도구 점검 3판 — 2026-11-05 03시 (벤치마크 루프 대상 5)

**사용량 비상(today.md 11/4 21:33, 11/5~11/8 21:00) 중 회차.** today.md를 회차 첫머리에 읽지 않아 조사를 일부 돌린 뒤에야 쉼 줄을 봤다. 그 뒤 추가 조사는 멈췄다. 아래는 이미 돌린 결과만 적은 것이다. 새 지시는 11/8 21:28 회의 뒤로 미룬다.
10/24·10/30 회차(대상 5) 파일은 없다. PC 절전·정지 기간이라 돌지 않은 것으로 본다(확인 안 함).

## ① 지난 개선 반영 — 5/5
| 개선점(1018·1019) | 상태 | 근거 |
|---|---|---|
| ytlong에 C-readback 관문 | 반영 | ytlong.py:55 readback_check, :114에서 gate가 부름 |
| 합의오독 표시 | 반영 | lfvoice.py:620 `AGREE, OFF = 0.9, 0.85` |
| C-2 '도,'·'안이었거든요'·'고른 길' 다시 받기 | 반영 | C-2 say_v3.txt 18·107·126행 = 문장 쪼개기·'넘지 않았거든요'·'고른 방법이' |
| '안이었다' 대본 금지 | 반영 | 최근 편 K-1·P-4·H-4·P-3 grep 0건(C-2 옛 판에만 남음) |
| 1019 추천: RealVisXL 실사 장면 시범 | 반영 | H-3 h3props.py:77 AIL, shot_plan 5장면(kold_s1·s2·key·school2·window) |

## ② 새 도구(10/6~11/5) — 공식 원문
- **FLUX 3 Image Klein**(BFL, 10/15): 5.6B, FLUX Kommunity License. 연매출 $5M 미만이면 결과물 상업 사용 가능(2.e 조건: 결과물 걸러 보기·법이 정한 AI 표시). 공식 최소 VRAM은 8GB(INT8)라 이 PC 6GB는 안 됨. HF Space(ZeroGPU)는 로그인 없이 됐고, 장당 약 10초 걸렸다.
- **Ming-3.0-tts-0.5b**(inclusionAI, 2026.10, MIT): 한국어 CER 1.728%(MiniMax 다국어 시험셋, 공개 모델 3위). VRAM 공식값 없음. 시험은 **막혔다**. Klein 3장으로 익명 ZeroGPU 하루 한도를 다 써서 "ZeroGPU quota exceeded"가 떴다. 그래서 **확인 안 함**.
- 제미나이(changelog 10/6~11/4): Nano Banana 2.1 정식 출시(무료 없음, 1K $0.0336). 3.1-flash-image는 사용 중단 예고. **Veo 3.1 미리보기는 10/22 종료**됐고 대체는 Omni Flash(무료 없음, 720p 초당 약 $0.10)다. → 1019 review의 '움직이는 컷은 Veo 3.1 Lite 5초 $0.25' 경로는 없어졌다. 지금 최저는 Omni Flash 5초 약 $0.50이다. 3.8 Flash·Flash-Lite TTS는 무료 등급이 그대로다(유료 단가는 2027-01-01부터 두 배). 11/4에 목소리 리믹스가 추가됐다(우리는 Chirp라 해당 없음).
- Qwen-Image-2.1(9/20): 연구용 라이선스(상업 금지)라 탈락.
- 우리 코드에 걸리는 것: `gemini-2.5-flash-preview-tts`는 11/17 종료인데 research/sonpum2/tour_voice.py:10 후보 목록에만 있다. `gemini-3.1-flash-image`는 썸네일 시험 gen.py 6개에 있다(무료 0이라 지금 쓰지 않음). 둘 다 업로드 경로 밖이다.

## ③ 실사 기준 장면 — 같은 프롬프트(sdxl_gen.py PROMPTS), 지금 것 vs 새 것
파일: strategy/ai-footage-1019/clips/*__flux3-klein-hfspace.mp4(render.sh 그대로, 5초)·_pub/ 원본. 커밋하지 않았다.
| 장면 | RealVisXL V5(지금) | FLUX 3 Klein(새) | 판정 |
|---|---|---|---|
| 부부 공원 | 기와 처마·안개, 두 사람 체형이 같아 '두 노인'으로 읽힘 | 남녀 구분 분명, 손·발 정상, 낙엽 길. 길 위에 뜻 없는 검은 얼룩 1곳, 단풍 채도가 조금 높음 | **Klein 나음** |
| 아파트 저녁 | 저층+고층+산, 한국 같음 | 프롬프트대로 눈높이 산책로·흰 20층 판상형. 그런데 확대하면 **파란 번호판·중국 차 앰블럼** | **RealVisXL 유지** |
| 은행 손 | 뜻 없는 기호·바코드 | 손가락 정상. 그런데 서식에 **영어 'ACCOUNT OPENING FORM'**이 또렷함(Klein엔 negative 칸이 없음) | **RealVisXL 유지** |
- 움직임(4.9초 끝 프레임): 세 장면 모두 뭉개짐 없음.
- 결론: 기본 도구는 RealVisXL을 유지한다. Klein은 **사람 뒷모습 장면에 한해 두 번째 후보**로 쓴다(익명 하루 약 3장, 프롬프트에 'Korean license plates·blank paper, no printed text'를 더해 다시 시험할 것). 교체 지시는 하지 않는다(1/3만 나음).

## ④ 성과 — 판단 못 함
ytanalytics recent 30(11/5 03시): H-3 gvlX2KQcI8g(AI 실사 5장면) 조회 585·평균 시청 비율 12.87%. 같은 표의 롱폼 420buEFKB8k 30.94%·mkAxQPGaDqc 36.05%보다 낮다. 그러나 주제·길이가 달라서 AI 장면 효과로 가를 수 없다. 장면 구간 곡선은 사용량 비상이라 보지 않았다.

## ⑤ AI 티(그림) — 새로 본 것
- G1 실사 AI 장면의 차 번호판·앰블럼이 외국 것(Klein 아파트: 파란 번호판). 차가 보이는 장면은 확대해서 본다.
- G2 negative 칸이 없는 모델은 서류에 영어 제목을 또렷하게 그린다. 서류 장면은 'blank'를 명시하거나 흐린다.

## 결재(돈·가입·다운로드) — approvals.md엔 아직 안 올림(11/8 뒤 회의 안건)
- HF 무료 계정(가입): ZeroGPU 하루 2분 → 5분. Klein·Ming 시험이 하루 3장 벽에 막힘.
- Ming-3.0-tts-0.5b 가중치 다운로드(무료, 크기 확인 안 함). 6GB에서 도는지 공식값 없음.
- 움직이는 실사 컷: Veo Lite 경로 종료 → Omni Flash 5초 약 $0.50(결제 필요).

## 출처
bfl.ai/blog/flux-3-image-klein · huggingface.co/black-forest-labs/flux-3-image-klein(LICENSE.md) · github.com/inclusionAI/Ming-3.0-tts(README·LICENSE) · ai.google.dev/gemini-api/docs/changelog·pricing(→aistudio.google.com/docs, 11/5 열람) · huggingface.co/Qwen/Qwen-Image-2.1(LICENSE)
