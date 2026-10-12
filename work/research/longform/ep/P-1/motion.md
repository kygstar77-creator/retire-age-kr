# P-1 모션 설계 (firemap-motion-designer)

## 10/12 실사 장 머리 StockShot — 1장·4장·5장·6장 (사장님 10/11 "다른 애들도 다 장면 넣고 있구만")
- 미리보기: motion_preview/p1_stock.mp4(960x540, 4장 × 3.5초) · 묶음 board_stock.png · 심사 review_stock.md
- 재료: `py -3.12 work/research/longform/ep/P-1/motion_preview/stockprops.py` → p1_stock.json + work/video/public/stock/ 복사 (장 제목 = script.md '## N. 제목' assert, 칩 = facts.txt/script.md 원문 assert)
- 컷(얼굴·국적·글자·연도·상표 없음, Pexels): 1장 생일 케이크 촛불 19875346 / 4장 낙엽 길 발걸음 34418451 / 5장 노트북 치는 손 18835800(상표 블러) / 6장 서류·계산기 7593893(뒷모습)
- 칩: 1장 '1969년생부터 65세' · 4장 '65세 기대여명 남 19.5년 · 여 23.7년 (평균일 뿐)' · 5장 '국민연금법 제63조의2 · 2026-06-17 시행' · 6장 '신청 없이 7월 말부터 환급'
- 글자 쪽: 왼 · 오 · 왼 · 오 (반복 템플릿 방지)

### PD가 할 일(녹음 뒤)
1. P1.tsx(만들 때) 장 1·4·5·6 첫 장면 앞에 `<StockShot {...shots[i]} />`를 Sequence로 3.5초(105프레임). 장 첫 말 줄을 그 위에 깔고 싶으면 dur = 그 줄 frames(8초 넘기지 말 것, U5).
2. 설명란 끝에 출처 4줄 — stockprops.py 실행 출력 '설명란 줄(PD)' 그대로(credits.json desc_line, used=true).
3. 렌더 뒤 `lfrender.py screen`: 장 머리는 화면 전체가 바뀌어 새 화면으로 잡힘.
4. AI 실사 아님(실제 촬영 스톡) → containsSyntheticMedia 해당 없음.

### '8초 안에 판 바뀜' 설계(다음 회차)
- 1장 계단 달력(5묶음)·2장 점수판 세 칸·5장 계단 그래프가 말 2~3줄 동안 같은 판 → U5 위험. 다음 회차에 말 줄마다 바뀌는 시점 표를 여기에 적는다.
