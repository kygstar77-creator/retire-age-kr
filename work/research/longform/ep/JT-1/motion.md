# JT-1 모션 — 받은 돈 합 경주 → 차 언덕(SumRace) (2026-11-16 motion)

shot_plan 3장 줄 '받은 돈 합 두 선이 그려지며 93세에서 만나는 그래프, 만나는 점에 손 동그라미'(visual 판 jt1_cross93·jt1_mid3 자리)를 움직이는 판 두 장면으로 만들었다. 나머지 판은 visual 종이 판(jt1boards.py) 그대로. 쓸지는 PD가 고른다.

| 장면 | 부품 | 말 줄 | 무엇이 움직이나 |
|---|---|---|---|
| race '받은 돈 합 · 65세 vs 70세' | video/src/motion/SumRace.tsx | 3장 '그럼 못 받은 7,600만원을' ~ '그러면 93세가 됩니다' 3줄 | 나이 바늘이 65세→93세 앞까지 걸으며 두 합 선·결 면을 그림(70세 쪽은 70세까지 0) → 70세 괄호 '못 받은 7,584만원' → 만남 '?' → '23년' 가로 괄호 → 손 동그라미 + 주황 '93세' |
| gap '65세에 든 쪽이 더 받은 돈' | 같은 부품(lam 0→1) | '중간을 끊어 보면' ~ '그러니 93세보다 오래 사시면' 6줄 | 70세 쪽 선을 빼서 바닥 점선으로 눕힘 → 틈이 언덕(꼭대기 7,584만원)으로 커짐 → 80·85·90세 점·기둥 '4,284·2,634·984만원'이 말 따라 주황(그 나이~93세 남은 앞섬 면 연주황) → 93세 바닥선 만남 → 마지막 줄 93세 뒤 띠 '이 뒤로는 70세 쪽이 더' |

- 왜 둘로 나눴나(첫 렌더 눈 검사): 5억 축 한 장에서 두 선 차(최대 7,584만원)는 70px — 80·85·90세 괄호가 선에 묻혀 안 읽혔고 같은 판 32초. 차를 직접 그리는 gap으로 바꿈.
- 숫자: jt1props.py가 calc_out §1(1,264천·1,539천·7,584만원·23.0년·93.0세)·§7(80·85·90세 합과 차)을 assert. 모든 점 = 월지급금 × 받은 달 수(집값 그대로 가정). 만남은 두 직선 교점 92.98세, 글자만 '93세'. 말은 '4,300·2,600·1,000만원 정도', 화면은 calc 원값(대본 자막과 같은 값).
- 미리보기: motion_preview/jt1_race.mp4(31.5초, 어림 길이) · 줄별 스틸 board_race.png·board_gap.png(jt1_st/) · U5 최장 6.0초·8초 넘는 곳 0 · UI 상자 0/9.
- 쓰는 법(PD, 11/17 녹음 뒤): ① `py -3.12 work/research/longform/ep/JT-1/motion_preview/jt1props.py`(voice.json 있으면 그 길이로, 줄 바뀌면 assert로 멈춤 → cut() 시작·끝 문구만 고침) ② JT1.tsx 장면 kind 'race'·'gap'에 `<SumRace {...s.data} beats={tallyStarts(s.lines)} />`(TallyFrame 자식, title·source는 jt1_motion.json) ③ 렌더 뒤 그 구간 lfrender screen·overlap. 부품 안 글자는 screen_text 밖 → 편집 서명 때 jt1_st/ 스틸을 같이 본다. 미리보기 렌더는 `jt1render.py`(작은 public — C: 남은 자리 8GB, public 11GB 통째 복사는 ENOSPC).
- 심사(motion_preview/review_jt1.md): 제미나이 race 9·gap 9 / Claude 새 심사관 1차 7·6 → 고침 → 2차 8·7 → 마지막 지적(뒤 칸 글자 자리) 고침. 통과선 6.
