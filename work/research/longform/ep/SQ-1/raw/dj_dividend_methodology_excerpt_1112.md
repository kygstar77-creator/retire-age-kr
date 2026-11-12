# S&P DJI "Dow Jones Dividend Indices Methodology" — September 2026 (발췌)
원문: https://www.spglobal.com/spdji/en/documents/methodologies/methodology-dj-dividend-indices.pdf (78쪽, 표지 'September 2026')
받은 방법: 내장 브라우저에서 S&P DJI 방법론 글(https://www.spglobal.com/spdji/en/methodology/article/dow-jones-dividend-indices-methodology/)의 PDF 링크를 페이지 안 fetch → pdf.js로 글자 추출, 2026-11-12 20:5x KST. 자동 curl은 403.
쪽 번호는 PDF 쪽(문서 아래 인쇄 쪽 번호는 1 작음: PDF p31 = 인쇄 30쪽).

## PDF p31~32 (인쇄 30~31쪽) Dow Jones U.S. Dividend 100 Index — 요지 (영어 원문 문장은 복사하지 않고 규칙만)
- 대상: Dow Jones U.S. Broad Stock Market Index 구성 종목, 리츠 제외(GICS 6010·402040).
- 거르는 조건 3개: 배당 10년 연속 지급 · 유동 시가총액 5억 달러 이상 · 3개월 하루 평균 거래대금 200만 달러 이상.
- 통과 종목을 배당수익률(IAD÷주가, 특별배당 제외) 순으로 세워 위쪽 절반만 남김.
- 남은 종목을 4개 항목으로 각각 순위: ① 잉여현금흐름÷총부채(부채 0이면 1등) ② ROE ③ 배당수익률 ④ 5년 배당 성장률 → 네 순위 합으로 종합 점수.
- 종합 점수 상위 100개 편입. 완충 규칙: 기존 종목은 200위 안이면 남김, 빈자리는 새 종목을 순위대로.
- 기준일: 배당 이력·재무는 12월 마지막 영업일, 시가총액·거래대금·배당수익률 주가는 2월 셋째 금요일.
- 비중: 분기마다 유동 시가총액 가중, 한 종목 4.0% 상한, 한 업종(GICS 섹터) 25% 상한.
- 매일 점검: 4.7% 넘는 종목들의 합이 22%를 넘으면 다시 맞춤(이틀 뒤 반영).

## PDF p49 (인쇄 48쪽) Index Maintenance — Rebalancing
- 아래 따로 적은 지수를 빼고는 매년 1회 재구성, 3월 셋째 금요일 다음 월요일 장 시작에 반영. (U.S. Dividend 100은 예외 목록에 없음 → 매년 3월)
- 주식 수는 재구성 12영업일 전 가격으로 정함.
