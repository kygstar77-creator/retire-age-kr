# PD(영상 제작) 교본 — firemap-video-producer

## 체크리스트(편마다)
- [ ] script.md.edit.json(편집 통과) 확인 뒤에만 목소리
- [ ] 한 편 = 한 TTS 모델·한 목소리(Charon), 429면 모델 바꾸지 않고 다음 초기화(16:00)
- [ ] TTS 한도 전 남는 시간엔 **화면 먼저**(<편>props.py + <편>.tsx, 목소리 없을 땐 초당 5.5음절 어림) — E-2·N-1·R-1 이렇게 함
- [ ] props.py 안 숫자는 facts.txt 원문 줄과 need()로 기계 대조
- [ ] 스틸: `node stills.mjs <ID> <id>.json out/<id>_stills_HHMM` → 끝 프레임 6장씩 붙인 판으로 눈 검사(자막 3줄 = 아래 ~250px 가림 주의)
- [ ] 렌더 뒤 deess·clickscan·motioncheck → ytlong gate → 예약(19~21시)

## 잘된 우리 사례
- D-1: 목소리 70/70 · readback 오탐 확인 · deess −13.7dB · gate 통과 · 예약 업로드(GMc2Rd1-JYA)

## 실패 사례
- E-2(10/2): 목소리 시작 뒤 화면이 없어 관문 기한 넘김 → 이후 화면을 먼저 만드는 순서로 바꿈
- 묶음 앞머리 지시문을 TTS가 읽어 문장 파일이 한 칸씩 밀림 → fixcut·readback 필수

## 배운 것(회차마다 1줄)
- 2026-10-03 R-1: 자막이 3줄이 되는 장은 화면 아래 y≈830부터 가려진다 — 축 글씨·칩은 y≤760에 둔다. 한 문장이 긴 장은 단계 시점을 문장 번호 대신 장 길이 비율(0.42·0.7)로 잡는다.
