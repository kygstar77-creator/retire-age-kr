# N-3 모션 — 움직이는 판 둘 (2026-10-29 motion)

shot_plan '장면 계획'의 움직이는 판 중 두 개를 부품으로 만들었다. 나머지 판(사다리 표·폭포·도넛·계단·블록·줄 100명)은 visual 몫 그대로(TallyFrame 판).

| shot_plan 줄 | 장면 | 부품 | 말 줄 | 무엇이 움직이나 |
|---|---|---|---|---|
| r19 3장 연금 상한 | cap | video/src/motion/CapStop.tsx | 3장 '그런데 국민연금에는 끝이 있어요' ~ '이게 다음 장에서' 5줄 | 3천~8천 막대가 차례로 자람 → '659만원' 말에 천장 점선 → 1억·1억 2천·1억 5천이 천장에 부딪혀 멈춤 → '31만원' 말에 주황 '31만원에서 멈춤' + 손 동그라미 |
| r37 7장 평균 깃발 | mean | video/src/motion/MeanPull.tsx | 7장 '평균도 마찬가지예요' ~ "그래서 '평균 연봉'은" 7줄 | 돈 자 그어짐 → 평균 4,475만원 깃발 → 중간값 3,417만원 깃발 → 자 너머 '상위 1%' 추(평균 3억 4,630만원)가 줄로 평균 깃발을 당겨 기울임 → 답 줄에서 줄이 느슨해지고 깃발이 서며 '약 1천만원 차이' |

- 숫자: n3props.py가 script.md·calc_out.txt·research.md에서 assert(연금 막대 = calc_out '연금 N' 원 단위 그대로, 상한 313,020 = 659만원 × 4.75% 10원 미만 버림). 새 숫자 없음.
- 정직성: 천장이 없었다면 얼마였을지(유령 막대)는 안 그림. 평균 깃발 자리는 옮기지 않음, 답이 열릴 땐 줄을 풀어 '1천만원 차이 전체가 1% 탓'으로 안 읽히게 함(Claude 심사 지적 — 아래).
- 미리보기: motion_preview/n3_motion.mp4(40.8초, 어림 길이) · 줄별 스틸 board_cap.png·board_mean.png · motioncheck 통과(움직임 51%·최장 정지 4.2초) · U5 최장 6.5초·8초 넘는 곳 0.
- 심사(motion_preview/review_n3.md): 제미나이 cap 9·mean 9 / Claude(새 심사관+레드팀) 1차 cap 7·mean 5(틀림: 오해 유도) → 고침 → 2차 cap 7·mean 6 → 마지막 지적 2개('그대로' 남음·제목) 고침. 평균 cap 8.0·mean 7.5, 통과선 6.

## PD 넣는 법(녹음 뒤)
1. `py -3.12 work/research/longform/ep/N-3/motion_preview/n3props.py` — voice.json이 있으면 그 길이로 n3_motion.json을 다시 만든다. 대본 줄이 바뀌면 assert로 멈춤 → cut() 시작·끝 문구만 고침.
2. N3.tsx 장면 kind 'cap'·'mean'에 `<CapStop {...s.data} beats={tallyStarts(s.lines)} />`·`<MeanPull {...s.data} beats={tallyStarts(s.lines)} />`(TallyFrame 자식, title·source는 n3_motion.json 그대로).
3. 렌더 뒤 그 구간 lfrender screen·overlap. 부품 안 글자는 screen_text에 안 들어감 → 편집 서명 때 n3_st/ 스틸을 같이 본다.

# 11/1 motion — 움직이는 판 둘 더(r18 블록 쌓기 · r28 거꾸로 계단)

| shot_plan 줄 | 장면 | 부품 | 말 줄 | 무엇이 움직이나 |
|---|---|---|---|---|
| r18 3장 블록 | blocks | video/src/motion/PayBlocks.tsx | 3장 '세금이 보험료보다 많아지는 건' ~ '보험료 네 가지는' 2줄 | 연봉 3천·5천·7천·8천 칸에 회색 보험료 블록 넷이 떨어져 쌓임 → 검은 소득세(+지방) 블록 → 보험료 윗선 점선(평평) → 소득세만 주황 + 가파른 손 선 + 8천 손 동그라미 |
| r28 5장 계단 | stairs | video/src/motion/RaiseStairs.tsx | 5장 '통장 400만원이면' ~ '통장을 같은 100만원씩' 10줄 | 통장 300(4,100만원) 칸 서 있음 → 400·500·600 칸이 말 따라 솟고 연봉 '?' → 열림 → '칸 사이' 줄에 더 솟은 부분 진하게 + 흰 '+1,580만원'·'+1,650만원' → '+1,770만원'만 주황·손 동그라미 → 끝 줄 '+100만원' 셋 |

- 숫자: n3props.py가 calc_out 'A' 줄(공제 내역 원 단위 ÷ 세전)·'I' 줄(통장 목표별 연봉)·대본 자막(칸 사이 1,580·1,650·1,770)을 assert. blocks 칸은 연금 상한 아래(8천까지)만 — 1억 위는 '같은 비율'이 깨져 뺌. 화면에 % 글자 없음.
- 정직성: 계단 바닥은 0원이 아니라 첫 칸 연봉 4,100만원(첫 칸 글자). 솟은 높이 = 연봉 차 비례.
- 미리보기: motion_preview/n3_motion2.mp4(37.5초, 어림 길이) · 줄별 스틸 board_blocks.png·board_stairs.png(n3_st2/) · motioncheck 통과(움직임 55%·최장 정지 4.8초) · U5 최장 5.0초·8초 넘는 곳 0.
- 첫 렌더 눈 검사로 고친 것: 칸 이름이 아래 출처 줄과 겹침(BASE 840→790·780) · 맨 위 '9,100만원'이 제목에 닿음(솟는 높이 470→390) · '칸 사이' 줄에서 답 주황이 먼저 켜짐(그 말에서만) · 손 선 시작점 주황 점.

## PD 넣는 법(녹음 뒤) — cap·mean과 같음
1. `py -3.12 work/research/longform/ep/N-3/motion_preview/n3props.py` (blocks·stairs도 같이 나옴, 줄 바뀌면 assert)
2. N3.tsx 장면 kind 'blocks'·'stairs'에 `<PayBlocks {...s.data} beats={tallyStarts(s.lines)} />`·`<RaiseStairs {...s.data} beats={tallyStarts(s.lines)} />`(TallyFrame 자식, title·source는 n3_motion.json). shot_plan 파일 칸(bg/n3/board/n3_blocks.png·n3_rev_steps.png)은 이 장면 스틸로 대신.
3. 렌더 뒤 그 구간 lfrender screen·overlap. 부품 안 글자는 screen_text 밖 → 편집 서명 때 n3_st2/ 스틸 같이.

## 11/4 blocks 말 줄 바뀜 반영
- 대본 3장 첫 줄 '낮은 연봉은 보험료가…' → '세금이 보험료보다 많아지는 건 연봉 8천 칸부터예요.'(youtube-loop 11/1 20:44) · n3props.py has()/cut() 시작 문구 고침 · 줄 2개 그대로(3.9·6.2초 어림).
- PayBlocks에 선택 칸 circleAt 더함(없으면 예전대로 가파른 선 뒤) · N-3은 0.8 = 첫 줄 '8천 칸부터예요' 끝에 8천 칸 손 동그라미(10.1% > 9.4%가 말과 같은 때 보이게).
- 미리보기 motion_preview/n3_blocks_1104.mp4(blocks 10.5초) · 눈 확인: 100프레임에 동그라미 시작·117프레임 다 그림, 숫자 글자 바뀐 것 없음. 심사 점수는 11/1 blocks 8.0 그대로(시점만 바뀜, 새 심사 안 함).
