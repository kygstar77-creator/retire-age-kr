# site-ia 시안 범위 확인 — firemap-designer (2026-10-01 22:16)

근거: plans/site-ia.md 6장(S1~S5)·0·3·9장, src/ui/ListRow.jsx(DS-6), src/ui/fm-ds.css 134~154행, src/components/firemap/MenuAll.jsx 37~47행. 브랜드 디렉터 확인은 별도(이 파일은 디자이너 몫만).

## 판정: 범위 통과 (조건 3) — 화면 캡처 검수는 S1·S2 시안 때

| 확인 항목 | 결과 | 근거 |
|---|---|---|
| 부품 30개 안 | 통과. S1 = ListGroup+ListRow(DS-6), S2 = MenuAll이 이미 쓰는 ListGroup(label)+ListRow 순서만 바꿈, 3번 버튼 = calc-3 [지시]와 같은 부품. 새 부품 0 | ListRow.jsx 1행, MenuAll.jsx 40~43행 |
| 행동 1 | 조건부 통과. 주황은 '계산하기' 하나 — 코너 행은 `accent` 끄고(기본값 false), trail은 chevron만 | fm-ds.css 154행(accent면 trail이 주황) |
| 숫자 1 | 첫 화면 숫자는 바뀌지 않음(행은 숫자 없는 제목만, toolPages.js title 그대로) | 6장 1번 |
| 이름·로고 불변 | 확인. 6장 '하지 않는 것'에 도메인·이름·로고·주소 이동 명시, 묶음 이름은 화면에 안 씀(3장) | 3·6장 |
| S3~S5 | 1판 범위 밖 맞음(S3 재심사 뒤·S4 예술가 뒤·S5 허브 판정 뒤, S5는 비주얼 디자이너) | 6장 |

## 조건 (S1 시안에서 잰다)
1. 코너 행은 ListRow size **S**, lead 아이콘 없음, desc 없음, accent 없음 — 4행이 버튼 아래 한 덩어리(ListGroup 하나). 이유: M 4행이면 약 200px로 계산하기 아래 공간을 다 먹는다. S면 행당 약 43px(10px×2+제목 줄+선 1px, 식 계산 — 화면 확인 안 함).
2. 첫 3초 기준(2장): 375×812·320×568에서 **'계산하기' 버튼 아래 끝 + 첫 코너 행 1개가 스크롤 없이** 보이는지 캡처로 잰다. 지금 첫 화면 버튼 위치는 이번에 재지 않음(확인 안 함 — dev 서버 꺼져 있음).
3. S2 '전체' 묶음 제목: MenuAll.jsx에 이미 있는 sec.label은 그대로 두고 순서만 3장 표대로. 새 묶음 제목은 editor-web 통과분만(3장).

## 다음
- S1·S2 시안(spec.md+preview.html 375·320)은 다음 근무 첫 조각 — 시한 10/2 12:00 안.
