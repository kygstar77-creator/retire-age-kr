# 조회 적은 공개 롱폼 썸네일 교체 — 효과 재기 (2026-10-19, 썸네일 담당)

사장님 10/19: "조회수 안 나오고 있는 영상들도 썸네일 바꿔 봐."
기준 자료: rethumb-1019.csv('before' 줄, 10-19 13:18). 다시 재는 법: `py -3.12 work/ytreach.py` 다음 `py -3.12 work/research/growth/rethumb_1019.py after`(예약 작업 firemap-rethumb-1019-recheck, 10/26 10:00 한 번).

## 바꾼 13편 (썸네일만, 10-19 13:3x · 영상·제목·설명 그대로)
| 편 | 영상 | 조회(10/19) | 노출 10/10~16 · 클릭률 | 제미나이 지금→새 | 새 판 |
|---|---|---|---|---|---|
| W-1 1화 | 0yWQeW38UJE | 4 | 20 · 0% | 5 → 8 | ep/W-1/thumb_r19a.png |
| W-1 2화 | AxTB7izIBUA | 7 | 6 · 16.7% | 6 → 8 | ep/W-1/w1016/thumb_r19b.png |
| G-1 | xBTZtRp5lMs | 3 | 12 · 8.3% | 5 → 8 | ep/G-1/thumb_r19b.png |
| P-1 | vsL7mojDW7w | 3 | 27 · 0% | 6 → 8 | ep/P-1/thumb_r19a.png |
| M-1 | eTjVs1vDTwg | 24 | 17 · 5.9% | 6 → 7.5 | ep/M-1/thumb_r19b.png |
| D-1 | GMc2Rd1-JYA | 113 | 14 · 21.4% | 5 → 7 | ep/D-1/thumb_r19b.png |
| E-1 | idc3JZOZukc | 26 | 21 · 0% | 6 → 7.5 | ep/E-1/thumb_r19a.png |
| E-2 | 7eD6SLt_jKc | 15 | 15 · 6.7% | 6 → 7 | ep/E-2/thumb_r19b.png |
| 6월 파이어 환상 | gSKsQWjTabo | 49 | 5 · 20% | 5 → 8 | ep/june-gSKsQWjTabo/thumb_r19b.png |
| 6월 배당금만으로 | cxls2Ve18-k | 40 | 2 · 50% | 5 → 8 | ep/june-cxls2Ve18-k/thumb_r19a.png |
| 6월 재능 없는 QQQM | JVTYZ208hgw | 122 | 5 · 0% | 5 → 8.5 | ep/june-JVTYZ208hgw/thumb_r19b.png |
| 6월 QQQM 하나 | wwfFszPl06g | 1,131 | 26 · 0% | 5 → 8 | ep/june-wwfFszPl06g/thumb_r19a.png |
| 6월 QQQM·SCHD | zhTjJwy1mwQ | 1,977 | 33 · 0% | 5 → 8 | ep/june-zhTjJwy1mwQ/thumb_r19b.png |

대조군(바꾸지 않음): scV67BQvC4Q(6월 '5억이면', 최근 7일 노출 471·클릭률 8.07% — 살아 있어 제외), A-1·N-1·H-1·R-1·N-2(지시로 제외). C-2는 오늘 따로 바꿔 대조군에서도 뺐다.

## 읽을 때 주의
- 바꾼 편들은 교체 전 7일 노출이 2~33회다. 이 정도 노출에서는 클릭률을 판단할 수 없다. 7일 뒤에도 노출이 수십 회면 "노출 부족, 판단 못 함"으로 쓴다.
- 노출 CSV는 이틀 늦다. 10/26에 재면 교체 다음 날(10/20)부터 10/24 무렵까지 5일쯤이다.
- 근거: 시안·심사 visual/rethumb-1019/(judge/*_score.md, understand_58.md, decisions.json, swap_log.json).
