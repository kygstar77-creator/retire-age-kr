# SQ-1 motion (2026-11-22 11:40 motion)
## 상시 장 띠 (registry B-57, 11/22 재판정 경쟁 5편 4/5)
- 부품: work/video/src/motion/ChapterStrip.tsx(오른쪽 위 'n장 이름 n/8' + 손 밑줄, KOSPI-1과 같은 부품).
- props: sq1_strip.json — 장 이름 8개는 script.md '## [n. 제목]'를 기계로 읽음(1 나스닥100은 어떻게 갈아 끼우나 … 8 끝). topic '나스닥100과 SCHD'. 적용 규칙은 파일 안 starts_rule.
- 자리: 오른쪽. 왼쪽 still에서 채널 꼬리표 '파이어맵'과 겹침(버린 시안) — 편 차이는 topic 글자로만.
- 미리보기(still, 렌더 없음): motion_preview/strip_chapter.png · 진입점 work/video/src/strip_sq1_index.ts(공용 Root 안 건드림). 화면 글자는 장 제목·대본 58행 한 줄뿐, 숫자 0.
- PD 할 일: SQ-1 편 tsx 맨 위에 <ChapterStrip chapters starts total=8 side='right' topic …/>, 실사 장면 dark. TallyFrame chapter 칸은 비운다. 0장 여는 말엔 띠 없음.
- 숫자 밀도(B-59 안 넣음): 3장 다섯 줄 표는 '한 줄씩 열림'이 대본에 있음 — 한 판이 14초 넘게 서면 줄 열림 사이에 다가가기(1.00→1.03)로 U5 8초 지킴.
- 11/26 motion: 3장 다섯 줄 표 포함 판 16장 U5 시뮬(PIL, inset·zoom 그대로) 최장 4.0초·끝 사진 2.0초 → 움직임 더 넣지 않음. '한 줄씩 열림'은 판 PNG가 한 장이라 없음(visual 판 판정 '나음' 그대로).
