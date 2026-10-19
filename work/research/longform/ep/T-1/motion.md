# T-1 모션 설계 (2026-10-19 motion)

## 2장 '보유만 한 1주택자만?' — 가로식 계산 세 장면(EqRow, 견본 방식 변주)
H-2는 세로 영수증(EqStack)이라 T-1은 **한 줄 가로식 + 계산기 키 칸**으로 바꿈(반복 템플릿 피하기). 주황은 답 하나, 답 '?' → 말이 닿을 때 열림 + 손 동그라미 한 번, 지난 식은 작은 회색 줄로.

| 장면 | 말 줄 | 무엇이 움직이나 | 지금 t1props 장면 |
|---|---|---|---|
| ratio '열두 배 가까이' | '같은 2029년에 수현 씨…' ~ '두 사람이 열두 배 가까이…' (2줄) | [1억 4,777만원] → ÷ → [1,241만원] → '열두 배'에 11.9배 | bars('2029년, 같은 20억 집') 대신 |
| year '살았던 한 해의 값' | '그럼 살았던 해 한 해는' ~ '이 값은 집마다 달라요' (3줄) | 거주 2년 − 3년 = 약 1,690만원('1,700만원쯤'에 열림) → 3년 − 4년 = 약 1,690만원 | bars('수현 씨 2029년 · 살았던 햇수별') 대신 |
| gap '한 해 차이마다 4%p' | '조심할 것도 있어요' ~ '수현 씨는 여덟 해 차이라서' (3줄) | 보유 40% + 거주 8% = 48% → 4%p × 8년 = 32%p → 48% − 32%p = 16% | 지금 그 3줄은 판 없음/다른 판 — PD가 고름 |

- 숫자: script.md [자막]·facts M4·calc_more_out 글자 그대로, 산술 assert(motion_preview/rowprops.py). 새 숫자 0.
- 미리보기: motion_preview/t1_row.mp4(39초) · board_ratio/year/gap.png · U5 최장 5.5초(1차 8.5초 1곳 → 다가가기 1.05·주황 바탕·키 칸으로 0).
- 넣는 법(PD): 녹음 확정 뒤 `py -3.12 work/research/longform/ep/T-1/motion_preview/rowprops.py` → t1_row.json의 ratio·year·gap data를 t1props 장면 kind 'mo'로, T1.tsx에서 `<EqRow {...s.data} beats={tallyStarts(s.lines)} />`(TallyFrame 자식). 줄 문구 바뀌면 cut() assert로 멈춤 → 시작 문구만 고침. 부품 안 글자는 screen_text 밖 → 편집 재서명 때 row_st/ 스틸 같이.
