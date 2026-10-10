# 무료 로컬 TTS 비교 — 2026-10-11 (영상 PD)

이 비교에서 제미나이 TTS는 한 번도 부르지 않았다. 제미나이 열은 이미 녹음돼 있던 C-1 파일을 다시 잰 값이다.

- 문장: C-1 `script.md`의 [0. 예고] 말하는 줄 12줄 전체(C-1 voice.json 0장과 같은 문장). 숫자는 한자어 읽기 한글로 바꿔서 넣었다(예: `1997년` → `천구백구십칠년`, `0원` → `영원`). `bench.py`의 `kor()`가 바꾼다. 제미나이 원본은 숫자를 그대로 읽은 녹음이다.
- 길이: 12줄이라 샘플이 50~70초다. 요청한 30~40초보다 길다.
- 재는 법(`bench.py`): `lfvoice.f0`로 줄마다 음높이 중앙값을 낸다. 앞뒤 무음을 자르고 RMS −20dBFS로 맞춘 뒤 잰다. 이 값으로 편 IQR/중앙(기준 ≤0.16)과 앞뒤 절반 평균 차(기준 ±7%)를 낸다.
- 말 속도: 대본 음절(lfvoice `syl`) ÷ (줄 길이 합 + 줄 사이 0.27초). lfvoice check의 '편 전체'와 같은 잣대이고, 목표는 5.5 이상이다.
- 재현성: 같은 12줄을 run1(seed 0)과 run2(seed 1)로 두 번 만들었다. 줄마다 음높이 차 |run2/run1−1|의 중앙값과 최대값을 쓰고, 편 중앙값 차를 함께 적는다.
- 받아쓰기: 제미나이 `gemini-3.5-flash-lite`로 받아썼다. TTS가 아니라 받아쓰기만 썼고, 3.5-flash는 429라 모든 후보를 lite로 같게 맞췄다. 대본과 다른 한글 글자 수를 셌다.
  - **받아쓰기 모델 자체가 틀린다.** 제미나이 원본도 15자(4.7%)가 걸렸다. '매도 씨'는 거의 모든 후보에서 '매도시'로 적혔고, '햇수'는 '횟수'로 적혔다.
  - 그래서 5% 안팎 차이는 구별하지 못한다. 서로 다른 단어로 들린 것만 '문제점'에 옮겼다.

## 표

| 후보 | 라이선스(원문 한 줄 · 링크) | 상업 이용 | 설치 | 생성 시간(RTX 3060 6GB) | 편 음높이 중앙 | IQR/중앙 (≤0.16) | 앞뒤 차 (±7%) | 음절/초 (≥5.5) | 재현성(같은 문장 두 번) | 받아쓰기 틀린 글자 | 샘플 |
|---|---|---|---|---|---|---|---|---|---|---|---|
| **제미나이 원본** (gemini-3.8-flash-tts · Charon, C-1 10/9~10/10 녹음) | — (지금 쓰는 것) | — | — | 하루 10요청 한도 | 151.7Hz | **0.212 ✗** | −2.1% | 6.34 | 이번엔 잴 수 없음(TTS 호출 금지). 기존 기록: 요청 안에서도 142~209Hz | 15/319 (4.7%) · 7줄 | `samples/gemini.wav` |
| **CosyVoice 3** (Fun-CosyVoice3-0.5B-2512, zero-shot) | 모델 카드 `license: apache-2.0` — [HF 모델 카드](https://huggingface.co/FunAudioLLM/Fun-CosyVoice3-0.5B-2512) · 코드 Apache-2.0 [LICENSE](https://github.com/FunAudioLLM/CosyVoice/blob/main/LICENSE) | 가능(Apache-2.0, 아래 주의 2) | 성공 | 53초 분량에 약 270초(RTF 5.1, fp32) · 첫 로드 103초 | 155.9Hz | **0.073 ✓** (run2 0.144 ✓) | **−0.0% ✓** (run2 +3.1% ✓) | **5.99 ✓** (run2 5.93) | 줄마다 중앙 7.2%·최대 17.1% 다름, 편 중앙 −7.6% | 16/319 (5.0%) · 8줄 | `samples/cosyvoice3.mp3` |
| **CosyVoice 2** (CosyVoice2-0.5B, zero-shot) | 모델 카드 `license: apache-2.0` — [HF 모델 카드](https://huggingface.co/FunAudioLLM/CosyVoice2-0.5B) | 가능(Apache-2.0, 아래 주의 2) | 성공 | 60초 분량에 약 246초(RTF 4.1) | 148.5Hz | 0.132 ✓ (run2 0.095) | −4.4% ✓ | **5.18 ✗** (run2 4.45) | 줄마다 중앙 7.8%·**최대 40%**, 줄 길이가 들쭉날쭉(4.4초 줄이 10.4~14.8초) | 23/319 (7.2%) · 10줄 | `samples/cosyvoice2.mp3` |
| **MeloTTS** KR, 빠르기 1.0 | 모델 카드 `license: mit` — [HF 모델 카드](https://huggingface.co/myshell-ai/MeloTTS-Korean) · README "free for both commercial and non-commercial use" [GitHub](https://github.com/myshell-ai/MeloTTS#license) | 가능(MIT) | 성공(윈도 고침 2곳, 아래) | 69초 분량에 GPU 16~24초(RTF 0.23~0.35) | **216.7Hz (여자 목소리)** | 0.068 ✓ | −4.5% ✓ | **4.64 ✗** | 줄마다 중앙 1.2%·최대 3.6% | 11/319 (3.4%) · 5줄 | `samples/melo.mp3` |
| **MeloTTS** KR, 빠르기 1.3(모델 안 길이 조절, atempo 아님) | 위와 같음 | 가능(MIT) | 위와 같음 | 56초 분량에 GPU 15~24초, CPU 69~83초(RTF 1.2~1.5 — 이 노트북에선 CPU 실시간 아님) | 223.0Hz (여자) | 0.077 ✓ | −3.5% ✓ | 5.71 ✓ | 줄마다 중앙 1.0%·최대 3.2% | 20/319 (6.3%) · 7줄 | `samples/melo_s1.3.mp3` |
| (참고만) **edge-tts** ko-KR-InJoonNeural | **약관 근거 없음 — 쓰지 않음.** 마이크로소프트 Q&A 답변(Microsoft External Staff · Moderator): "commercial use without a valid Azure subscription could be a violation of our terms of service" — [원문](https://learn.microsoft.com/en-us/answers/questions/2088770/are-opensource-edge-tts-free-for-commercial-use). [서비스 약관](https://www.microsoft.com/en-us/servicesagreement)에는 Edge 소리 내어 읽기를 따로 허용하는 조항이 없다 | 근거 없음 → 쓰지 않음 | 이미 설치됨 | 24줄에 24.5초(온라인) | 163.8Hz | 0.066 | −2.1% | 5.16 ✗ | 줄마다 0.2% | 12/319 (3.8%) · 7줄 | `samples/edge.mp3` |

## 후보별 문제점

### CosyVoice 3
- **목소리**: 참고 음성은 우리 E-1 제미나이(Charon) 녹음 두 줄(10.3초, 숫자 없는 줄)만 썼다.
  - 파일: `audio/e-1/c55eb53936ad18b7.wav`, `975b0847c10f73d3.wav` → `ref_e1.wav`
  - 결과는 155.9Hz로, 지금 목소리 높이(E-1·C-1 중앙 약 150Hz)와 비슷하다. 실제로 같은 사람처럼 들리는지는 **사장님이 들어 볼 것**.
- **받아쓰기에서 다른 단어로 들린 곳**(받아쓰기 오류일 수 있다):
  - 6번 줄: '환율' → '판유', '볼 건' → '물건'
  - 4번 줄: '차이인데' → '찬데'
  - 5번 줄: '년째' → '년재'
- **느리다**: RTF 5. 15분 롱폼이면 GPU로 약 75분이 걸린다. 한도가 없으니 밤에 돌리면 된다.
  - fp16·TensorRT는 시험하지 않았다(확인 안 함).
- **같은 줄도 만들 때마다 음높이가 다르다**: 줄마다 중앙 7%, 최대 17% 차이. 대신 편 단위(IQR·앞뒤 차)는 두 번 모두 기준 안이었다.
  - 무료·무제한이라, 튀는 줄만 다시 만드는 '다시 받기'가 공짜다. 지금 lfvoice `--gate`와 같은 방식을 그대로 붙일 수 있다.

### CosyVoice 2
- **줄이 길게 늘어진다**: 4~5초 줄이 10~15초가 됐다(run1 5·11번, run2 6·7·11번). 끝에 이상한 소리가 붙는 것으로 보인다.
- **숫자를 다르게 읽는다**: '십칠년째·십삼년째'를 '열일곱째·열셋째'로 읽었다. 받아쓰기에 '응?'이라는 군소리도 잡혔다.
- 그래서 속도도 기준 아래로 떨어졌다(5.18 / 4.45). CosyVoice 3가 있으니 2는 쓸 이유가 없다.

### MeloTTS
- **한국어 목소리가 여자 한 명뿐이다**(KR 화자 하나, 약 217Hz). 지금 채널 목소리(남자 Charon)와 다르다. 목소리를 바꾸려면 학습이나 별도 음색 변환이 필요한데, 시험하지 않았다(확인 안 함).
- **빠르기**: 1.0에서는 4.64음절/초로 기준에 못 미친다. 1.3이면 5.71로 통과하지만, 받아쓰기에서 다른 단어로 들린 곳이 늘었다.
  - 1.3 기준: '일년'→'이온', '십일년째'→'칠년째', '딱 일 년'→'딱 6년'
  - 1.0에서는 이 셋이 없었고, 대신 '세금이 영원이에요'가 '세금이에요'로 들렸다.
- **가장 한결같다**: 같은 문장을 두 번 만들면 음높이가 1~3%밖에 다르지 않다. 빠르기도 가장 빠르다(GPU RTF 0.3).
- 윈도에서 그대로는 돌지 않았다. 고친 곳 두 군데(모두 `.venv` 안이라 커밋하지 않음):
  1. 일본어 사전(unidic) 없이 import되게 `melo/text/japanese.py`의 MeCab 초기화를 try로 감쌌다.
  2. g2pkk가 윈도에서 eunjeon을 찾는 부분을 python-mecab-ko로 바꿨다. 이 패키지는 `.venv/mecabko`에 따로 설치했다. mecab-python3의 `MeCab` 폴더와 윈도에서 이름이 겹치기 때문이다.

### 제미나이 원본(비교용)
- 이 12줄만 재도 IQR 0.212로 관문(≤0.16)에 걸린다. 줄 음높이는 129~190Hz.
- 로컬 후보는 모두 0.07~0.13으로 이보다 덜 흔들린다.

## 주의
1. **제미나이 출력을 참고 음성으로 쓰는 문제**: 제미나이 API 약관 [원문](https://ai.google.dev/gemini-api/terms)에 두 문장이 있다.
   - "Google won't claim ownership over that content."
   - "You may not use the Services to develop models that compete with the Services"
   - 우리는 모델을 학습시키지 않고 참고 음성으로 넣기만 한다. 다만 이것이 위 조항과 무관한지는 **확인 안 함**이다. 걱정되면 사장님이나 팀원이 직접 녹음한 10초로 바꾸면 이 문제가 없어진다.
2. **CosyVoice 모델 카드 끝의 Disclaimer**: "The content provided above is for academic purposes only and is intended to demonstrate technical capabilities"라는 문장이 있다.
   - 앞 문장 뜻으로 보면 카드 위 예시·데모 내용에 대한 말이고, 가중치 라이선스는 `apache-2.0`으로 따로 적혀 있다.
   - 상업 이용을 막는 문구는 카드에서 찾지 못했다.
3. **CosyVoice 2·3는 남의 목소리를 넣지 않았다.** 참고 음성은 우리 E-1 녹음뿐이다.

## 추천: CosyVoice 3 (Fun-CosyVoice3-0.5B-2512)
- **목소리 관문**: 두 번 만들어 두 번 다 통과했다(IQR 0.073·0.144, 앞뒤 −0.0%·+3.1%).
- **속도**: 5.9~6.0음절/초로 빠르기를 따로 손댈 필요가 없다.
- **목소리**: 참고 음성으로 지금 채널 목소리(우리 E-1 녹음)에 맞출 수 있는 유일한 후보다. 높이 156Hz.
- **비용·한도**: Apache-2.0이고 하루 한도가 없다.
- **약점**:
  - 느리다(15분 편 약 75분).
  - 줄마다 흔들림이 있다(최대 17%). 받아쓰기 대조(readback)와 튀는 줄 다시 만들기를 꼭 붙여야 한다.
- MeloTTS는 가장 한결같고 빠르지만 **여자 목소리 하나뿐**이라 채널 목소리를 바꾸는 결정이 된다.

**사장님이 들어 볼 것**: `samples/gemini.wav`(지금) ↔ `samples/cosyvoice3.mp3`(추천) ↔ `samples/melo_s1.3.mp3`. 음질·자연스러움·발음은 숫자로 못 쟀다.

## 다시 만드는 법
```
py -3.12 work/tts_local/bench.py lines      # lines.json, ref_e1.wav
py -3.12 work/tts_local/bench.py gemini     # 기존 녹음 복사(TTS 호출 없음)
work/tts_local/.venv/cosy/Scripts/python work/tts_local/gen_cosy.py 3
work/tts_local/.venv/melo/Scripts/python work/tts_local/gen_melo.py --speed 1.3
py -3.12 work/tts_local/bench.py measure cosyvoice3
py -3.12 work/tts_local/bench.py hear cosyvoice3
```
- venv는 `.venv/melo`·`.venv/cosy`(py 3.10, torch 2.3.1+cu121, mkl 2021.4)이고, 모델은 `models/`에 있다. 둘 다 커밋하지 않는다.
- torch를 pip로 받다가 두 번 멈췄다. 그래서 curl로 16갈래로 나눠 받았고(ETag md5 일치), 받은 파일은 `models/wheels/`에 있다.
