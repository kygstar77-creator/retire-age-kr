# firemap-audit 교본 (품질·정책 감사관)

## 경쟁 1등 사례
- 확인 안 함 — 금융 유튜브·카페의 공개 정정 사례(고정 댓글 정정 등)를 다음 회차에 하나 찾아 적는다.

## 잘된 우리 사례
- 10/2: D-1 건보료 숫자를 공개 전에 직접 재계산(20,160→22,800, 54만원) — 원자료로 다시 계산해야 '맞다'고 쓴다.
- 10/3: 새 공개가 0편인 회차에는 오늘 나갈 묶음(slots.json 칸)을 공개 전에 감사했다 — 틀린 숫자를 공개 뒤가 아니라 앞에서 잡는 자리.

## 실패 사례
- 10/2: 롱폼 2편이 같은 날 공개된 것을 사후에야 잡았다(앞당김 지시). 앞당김이 있으면 그날 다른 예약을 같이 본다.
- 9/30 메모: 스꾸 애드센스 건에서 재지 않고 '정책 위반' 단정 → 틀렸다. 단정 전에 잰다.

## 체크리스트
1. today.md에서 audit 담당 [지시] 먼저.
2. 새 공개물 목록: 유튜브 uploads 재생목록 8편(status 3칸), cardshorts/log.jsonl, uploads.jsonl, */pkg/published.txt.
3. 새 공개 0이면 slots.json 오늘 칸 묶음을 공개 전 감사.
4. 사실 3건: facts.txt가 아니라 그 아래 원자료(law.txt·schwab_dist.txt·yh.json·rank_out.txt)로 직접 재계산.
5. 금지어 grep(c0*.txt), compare.md·review.md 유무.
6. naverpost.py AutomationControlled(주석인지), STOP_* 파일 상태.
7. 제목 틀 반복(쉼표 틀 비율), 같은 틀·같은 음악 연속.

## 배운 것(회차마다 1줄)
- 2026-10-03: 카드 쇼츠는 음성이 없어 'AI 음성' 표기 대상이 아니다(롱폼만 ytlong containsSyntheticMedia). 감사 전에 그 편에 음성이 있는지부터 본다.
