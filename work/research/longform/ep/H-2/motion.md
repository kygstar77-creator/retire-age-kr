# H-2 모션 설계 (motion) — 10/18 견본 방식

## 5장 '사려면 현금이 얼마나' — 장면 셋 (motion_preview/)
| 장면 | 줄 | 무엇이 움직이나 | 부품 |
|---|---|---|---|
| rule '대출은 둘 중 작은 쪽까지' | '먼저 대출 규칙입니다' ~ '25억이 넘으면 2억까지입니다' (5줄) | 0 집값 축·40% 경사+면 → 1 '둘 중 작은 쪽' 면(min 모양) → 2·3·4 한도 선 칸마다 굵게, 오른쪽 지금 칸 한도 하나만 주황 | LoanSteps phase rule |
| cash '손품 씨 계산서' | '이제 손품 씨 돈으로 계산합니다' ~ '래미안원베일리 약 59억이면' (5줄) | 집값 ? − 대출 2억 − 보증금 9억 5,000만원 = ? → 리센츠·주공5단지·원베일리 차례로 답 열림 + 손 동그라미, 지난 답 회색 칩 | EqStack ledger |
| edge '25억이라는 선' | '여기서 조심할 건 25억이라는 선입니다' ~ '그래서 25억 언저리 집을 볼 땐' (3줄) | 21~29억 확대, 점이 25억을 넘는 순간 4억 → ? → 2억 + '절반', 끝 줄 '은행이 보는 이 집 값은?' + '4억? 2억?' | LoanSteps phase edge |

숫자: facts [R1]·[R7]·calc_out 가운데 값·script [자막] assert(eqprops.py). 새 계산은 뺄셈 셋(자막 값과 같음).
미리보기 h2_eq.mp4(60.2초, 녹음 전 voice.json 길이) · U5 최장 6.5초 · 심사 review_eq.md.

## PD 붙이는 법
1. 다시 녹음 뒤 `py -3.12 work/research/longform/ep/H-2/motion_preview/eqprops.py` (줄 문구가 바뀌면 assert로 멈춤 → cut() 시작·끝 문구만 고침)
2. h2props 5장 해당 장면을 kind 'mo'(또는 새 kind)로: `<LoanSteps {...rule.data} beats={tallyStarts(s.lines)} />` · `<EqStack {...cash.data} .../>` · `<LoanSteps {...edge.data} .../>` (TallyFrame 자식, 판 board=true)
3. 렌더 뒤 그 구간 still_runs·overlap · 부품 안 글자는 screen_text에 안 들어감 → 편집 재서명 때 eq_st/ 스틸 같이

## 대본 확인 필요(youtube-loop·editor)
- script.md 5장 '집값이 25억 이하면 한도가 4억입니다' — 15억 이하는 6억(facts R1·R7). 레드팀: '15억 넘고 25억 이하면 4억'. 화면 라벨은 '15억~25억 · 한도 4억'으로 고쳤음.
- '은행이 그 집 값을 얼마로 보는지' — 25억 판정 기준 가격(시세·감정가)은 facts에 없음(레드팀 '확인 안 함').
