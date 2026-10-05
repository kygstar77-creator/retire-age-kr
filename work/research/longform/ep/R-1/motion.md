# R-1 모션 설계 (firemap-motion-designer)

## 첫 장면 open(0~23.4초) — '점 하나 → 줌아웃' 새 판 (2026-10-05)
| 말 | 프레임 | 무엇이 움직이나 |
|---|---|---|
| 1 통장에 1억이 들어왔다 | 0~149 | 1억 점 하나를 3.4배 확대한 채 시작, 55~75 '입금 +1억' 줄 진입, 아주 천천히 빠짐 |
| 2 예금? ETF? 금? | 149~330 | 카메라가 1배로 빠지며 갈래가 대본 순서(예금·S&P500·SCHD·금)로 '?'까지 뻗음 |
| 3 네 군데 똑같이 넣고 영수증 | 330~511 | 날짜 축 2025.10.2 → 2026.10.2, '1억' 넷이 같은 속도로 갈래를 따라감, '?'가 차례로 튐 |
| 4 세금이 간격 307만원 줄임 | 511~702 | 갈래 사라짐 → 가운데 막대: 세금 전 16,876,863원 → 세금 뒤 13,804,655원으로 줄어듦(길이 값 비례·0 기준선 공유), 빗금 '줄어든 몫 3,072,208원' |

- 정직성: 갈래 끝 자리는 고르게 나눈 자리(값 아님), 순서는 대본 순서 고정 — 결과 순위를 미리 암시하지 않음(레드팀 10/5 지적 반영). 숫자는 r1.json(=facts.txt 문구)·대조 assert(zoomprops.py).
- 부품 video/src/motion/ZoomOutOpen.tsx · 미리보기 motion_preview/open_zoom.mp4 · 비교판 board_open.png · 심사 review_open.md
- 실사 AI 장면 없음 → containsSyntheticMedia 해당 없음.

## [요청] firemap-video-producer — 본편에 넣을지 판단(심사 통과 시)
1. r1props.py open 장면 data에 줌아웃 재료 추가: zoomprops.py와 같은 값(names·nameAt·from·to·q·travel·gap·gapHead·pre·post·cut). **nameAt은 지금 글자 위치 어림** → 16:05 녹음 뒤 voice.json 문장 길이로 다시 돌리고 s_140~s_300 프레임을 눈으로 확인.
2. R1.tsx `case 'open'`을 `<ZoomOutOpen {...s.data.zoom} />`로 바꿈(기존 Open은 지우지 말고 남겨 되돌리기 쉽게).
3. 렌더 뒤 motioncheck · 0/2.5/7.7/14.7/23초 프레임 사실표 밖 숫자 0 확인.
- 안 넣는 경우도 손해 없음: 부품은 다음 편(M-1 월배당 등) 첫 장면 후보로 남는다.
