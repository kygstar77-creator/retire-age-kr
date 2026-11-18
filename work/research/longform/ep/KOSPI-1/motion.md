# KOSPI-1 모션 — 상시 장 띠·순위 범례 (2026-11-18 motion)
- 근거: registry B-57(경쟁 롱폼 8편 중 5편 상시 장·위치 표시, 62.5% > 문턱 60%).
- 부품: work/video/src/motion/ChapterStrip.tsx(오른쪽 위 '3장 이름 3/8' + 손 밑줄, 장 바뀔 때 써지듯 열림) · RankLegend.tsx(오른쪽 세로 범례, 말하는 칸 주황 점·손 밑줄, 지나간 칸 진하게).
- props: kospi1_strip.json — strip(8장 전부)·legend(3장 묶음 첫날 하락률 상위 6). 적용 규칙은 파일 안 starts_rule·on_rule.
- 미리보기(still, 렌더 없음): motion_preview/strip_chapter.png · strip_legend.png. 진입점 work/video/src/strip_index.ts(공용 Root 안 건드림).
- PD 할 일: KOSPI-1 컴포넌트(편 tsx) 맨 위에 <ChapterStrip …/>, 3장 장면에 <RankLegend …/>. TallyFrame chapter 칸은 비운다. JT-1·H-5에는 넣지 않는다.
- 금지 목록 점검: 알약·둥근 칸·테두리 상자·진행 막대 없음(점 하나·세로 선 하나만). 작은 글자 줄: 띠 2줄(주제·장) — 출처 줄과 합쳐 판 작은 글자 3줄, 경고 기준(쇼츠 ⑦)은 롱폼 해당 없음.
