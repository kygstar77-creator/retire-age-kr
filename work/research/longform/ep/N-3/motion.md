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
