# KOSPI-1 모션 — 상시 장 띠·순위 범례 (2026-11-18 motion)
- 근거: registry B-57(경쟁 롱폼 8편 중 5편 상시 장·위치 표시, 62.5% > 문턱 60%).
- 부품: work/video/src/motion/ChapterStrip.tsx(오른쪽 위 '3장 이름 3/8' + 손 밑줄, 장 바뀔 때 써지듯 열림) · RankLegend.tsx(오른쪽 세로 범례, 말하는 칸 주황 점·손 밑줄, 지나간 칸 진하게).
- props: kospi1_strip.json — strip(8장 전부)·legend(3장 묶음 첫날 하락률 상위 6). 적용 규칙은 파일 안 starts_rule·on_rule.
- 미리보기(still, 렌더 없음): motion_preview/strip_chapter.png · strip_legend.png. 진입점 work/video/src/strip_index.ts(공용 Root 안 건드림).
- PD 할 일: KOSPI-1 컴포넌트(편 tsx) 맨 위에 <ChapterStrip …/>, 3장 장면에 <RankLegend …/>. TallyFrame chapter 칸은 비운다. JT-1·H-5에는 넣지 않는다.
- 금지 목록 점검: 알약·둥근 칸·테두리 상자·진행 막대 없음(점 하나·세로 선 하나만). 작은 글자 줄: 띠 2줄(주제·장) — 출처 줄과 합쳐 판 작은 글자 3줄, 경고 기준(쇼츠 ⑦)은 롱폼 해당 없음.

## 11/19 겉싸개 StripOver — PD가 편 tsx를 고치지 않고 켠다
- 파일: work/video/src/motion/StripOver.tsx · 미리보기 진입점 src/stripover_index.ts(공용 Root 안 건드림).
- 쓰는 법: Root.tsx에 `const K1Strip = (p) => <StripOver inner={편 컴포넌트} p={p} strip={S.strip} legend={S.legend} />` (S = kospi1_strip.json). JT1.tsx·H5.tsx는 안 고친다(JT-1·H-5 같이 씀).
- 장 시작 = ask 장면 data.n 'N장'의 시작 프레임(자동). 범례 점 이동 = kospi1_strip.json legend.cues 글자로 시작하는 말 줄(대본 3장 114·116·118줄).
- 11/19 H-5 틀로 스틸 눈 확인(motion_preview/stripover_3looks.png, 위→아래 장 카드·실사·종이 판):
  1차에서 걸린 것 3개 → 고침: ① 장 카드(검은 바탕)에 진한 글자 → 흰 글자 ② pic 판 윗변(y≈38)과 띠 겹침 → 한 줄 20px top 2 ③ 범례가 pic 판 그래프 위에 → pic·ask·table·grid·rows에서 끔.
- 남은 확인: KOSPI-1 실제 props로 3장 끝 구간 still(PD props 생긴 뒤) — 띠 켤 때 TallyFrame chapter 칸 비우기는 PD props 쪽.
