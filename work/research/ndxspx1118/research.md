# ndxspx1118 자료조사 (11/19 22:40 카페 '새 주식·지수' 칸 — firemap-write-b 2026-11-18 16:5x~) — 나스닥100 vs S&P500, 하락장마다 누가 더 빠지고 언제 회복했나

## 검증
- 수요: kwvol 11/18 나스닥100 277,600 · S&P500 287,600 · QQQ 87,200 · TIGER미국나스닥100 28,020 · 나스닥100ETF 6,080 (kwvol_last.json) · 평생ETF 카페 주간 인기글 '고점 대비 하락률(KOSPI, S&P, NASDAQ)' 조회 50·댓글 7(raw/weekly_31097286.json, 같은 날 인기글 조회 중앙 96) · 블로그 상위 8편 중 7편이 11/4~11/18 작성(raw/toprank.txt)
- 겹침: 우리 제목 전수 나스닥·QQQ·지수 18편 — 보수(qqqm)·세금(qqqkr0927)·레버리지(levetf·qld0925)·코스피 하락(kospidd1022) · '나스닥100 vs S&P500 하락장 낙폭·회복' 각도 0편 · 11/19 07:40 SCHD 짝 글(배당)·18:40 부동산과 축 다름
- 경쟁에서 터진 증거: 11/16 나스닥 -2.49%(평생ETF 13606) 뒤 하락률 글이 주간 인기글에 · 블로그 8편 중 과거 하락장별 숫자 0편

## 원문
- S1 Yahoo Finance chart API ^NDX·^GSPC 일별 종가(1차 시세 자료, 가격 지수) — 2026-11-18 16:51 받음, 마지막 거래일 11/17 https://query1.finance.yahoo.com/v8/finance/chart/%5ENDX · https://query1.finance.yahoo.com/v8/finance/chart/%5EGSPC (raw/%5ENDX.json·%5EGSPC.json, calc.py·calc_out.txt)
- S2 Nasdaq-100 Index Methodology(1차) — 2026-11-18 16:56 PDF 본문 'Nasdaq-listed non-financial companies' https://indexes.nasdaqomx.com/docs/Methodology_NDX.pdf (raw/ndx_method.pdf)
- S3 Federal Reserve History 'The Great Recession and Its Aftermath'(1차, 연준) — 2026-11-18 16:56 '2007년 주택담보대출 관련 자산 손실이 금융시장 긴장으로', 2008년 9월 리먼 https://www.federalreservehistory.org/essays/great-recession-and-its-aftermath (raw/fed_gfc.html)
- S4 미래에셋자산운용 TIGER 미국나스닥100(H) 상품 정보(1차, 운용사) — 2026-11-18 16:56 '환헤지형으로서 원달러 환율변동율을 헤지' https://investments.miraeasset.com/tigeretf/ko/product/search/detail/index.do?ksdFund=KR7448300004 (raw/tiger_448300.html)
- S5 ETF쇼핑 '환헤지 vs 환노출 ETF 비교'(2차) https://etfshopping.com/lab/hedged-vs-unhedged (raw/etfshop_hedge.html)

## 경쟁
(bench.md 7편) 2·3·5위 '나스닥100 고수익·고변동, S&P500 하락 방어' 공식, 3·5위 운용사 공시 10년 연수익률(S&P500 15.3% 안팎·나스닥100 21% 안팎, 9/30 기준), 6위 11/13 고점 대비 하락률(나스닥100 -10.5%·S&P500 -3.3%), 1위 매달 30만원 적립. 빠뜨린 것: 과거 하락장별 낙폭·회복 기간 0편 · S&P500이 더 빠진 2008·2020 0편 · 하락 중 나눠 샀다면 0편

## 질문
1. 나스닥100과 S&P500 중 어떤 지수가 더 유리할까? — https://blog.naver.com/nmnpvv/224475364330 ('어떤 지수가 더 유리할까?') → 답: c03(10년 5.6배 vs 3.4배)·c04(다음 하락장은 모름)
2. 하락장에서 나스닥이 S&P500보다 더 빠지나? — https://blog.naver.com/18alsrb/224479650986 ('시장이 하락하면 알게된다') → 답: c00·c01(다섯 번 중 세 번)
3. 지금 고점 대비 얼마나 빠졌나? — https://cafe.naver.com/ca-fe/cafes/31097286/articles/13619 ('고점 대비 하락률(KOSPI, S&P, NASDAQ)') → 답: c03(11/18 종가 13.2%·6.3%)
4. 수익률만 보고 고르면 안 되는 이유는? — https://blog.naver.com/leemujeok/224474059614 ('수익률만 보고 선택하면 안 되는 이유') → 답: c02(회복 15년 7개월)·c04

## 왜
- 닷컴 때 나스닥100이 훨씬 더 빠진 이유: 거품의 중심이 기술주였음 — 원문 이유 확인 못 함(한계), 글에는 '차이가 크게 난 건 닷컴 한 번'까지만
- 2008년에 나스닥100이 덜 빠진 이유: S3 위기가 주택담보대출 자산 손실 → 금융시장, S2 나스닥100엔 금융회사가 없음
- 회복이 오래 걸린 이유: 바닥이 깊을수록 되돌아올 거리가 큼(83% 빠지면 5.8배 올라야 본전) — 계산
- 나눠 사면 빨리 본전: 값이 쌀 때 더 많이 사서 평균 단가가 내려감 — 계산(calc.py dca)

## 그래서
- 나스닥100 비중이 큰 사람: 닷컴 같은 기술주 중심 하락에선 회복에 10년 넘게 걸린 적이 있다는 걸 알고 비중을 정한다
- 한 번에 넣을지 나눠 넣을지: 닷컴 고점부터 매달 나눠 넣었으면 4년 9개월 만에 본전(한 번에 넣으면 15년 7개월) — 권유가 아니라 과거 숫자
- 국내 ETF로 사면 (H) 여부로 환율 영향이 달라짐을 이름에서 확인

## 누구라면
- 한꺼번에 목돈을 넣은 사람: 고점 회복 기간(c02)이 그대로 본인 기간
- 매달 적립하는 사람: 하락 중에도 계속 사면 본전이 더 빨리 옴(c03)
- 환헤지(H) 상품 보유자 / 환노출 상품 보유자: 원화 결과가 지수와 다름(c04)

## 함정
- 배당 뺀 가격 지수라 총수익(배당 재투자)과 다름 — 경쟁 3·5위 연수익률(총수익)과 숫자가 안 맞는 이유
- 원화 환율·보수·세금 미반영
- 다섯 번 하락장 원인이 달라 다음 하락의 크기는 알 수 없음

## 우리만
- calc.py: 1985-10-01~2026-11-17 일별 종가로 하락장 다섯 번 낙폭·회복 기간(나스닥100이 더 빠진 건 3번, S&P500 2번) · 닷컴 고점 달부터 나스닥100 매달 적립 본전 2004년 12월(2001년 10월 -51%, 2009년 3월 다시 -31%, 8월 회복) — 경쟁 8편 0편

## 예외
- 하락장 구간은 우리가 고른 다섯 번(닷컴·금융위기·코로나·2022·2025) — 1987년 블랙먼데이 등 다른 하락은 뺌
- 매달 적립 계산은 매달 첫 거래일 같은 금액, 수수료·환율 없음

## 한계
- 닷컴·2022년에 나스닥100이 더 빠진 이유는 1차 원문으로 확인 안 함 → 글에 이유 안 씀
- 11/17 하락(10/6 최고점 뒤 13.5%)의 원인은 조사 안 함 → 글에 안 씀
- Yahoo 지수 값은 시세 사이트 자료(지수 사업자 공식 파일 아님), 1985년 이전 나스닥100 없음
- 평생ETF 13619 본문은 회원 전용이라 못 읽음(제목·반응만)

## 대조
| 글 값 | 원문 값 | 출처 |
|---|---|---|
| 나스닥100 = 나스닥 큰 회사 100곳, 금융회사 뺌 | 'Nasdaq-listed non-financial companies' | S2 https://indexes.nasdaqomx.com/docs/Methodology_NDX.pdf |
| 닷컴 나스닥100 83%·S&P500 49% 하락 | 4,705→805 · 1,527→777 | S1 https://query1.finance.yahoo.com/v8/finance/chart/%5ENDX · https://query1.finance.yahoo.com/v8/finance/chart/%5EGSPC (calc_out.txt) |
| 금융위기 54%·57% | 2,239→1,037 · 1,565→677 | S1 https://query1.finance.yahoo.com/v8/finance/chart/%5ENDX · https://query1.finance.yahoo.com/v8/finance/chart/%5EGSPC (calc_out.txt) |
| 코로나 28%·34% | 9,719→6,994 · 3,386→2,237 | S1 https://query1.finance.yahoo.com/v8/finance/chart/%5ENDX · https://query1.finance.yahoo.com/v8/finance/chart/%5EGSPC (calc_out.txt) |
| 금리 인상 36%·25% | 16,573→10,679 · 4,797→3,577 | S1 https://query1.finance.yahoo.com/v8/finance/chart/%5ENDX · https://query1.finance.yahoo.com/v8/finance/chart/%5EGSPC (calc_out.txt) |
| 관세 충격 23%·19% | 22,176→17,090 · 6,144→4,983 | S1 https://query1.finance.yahoo.com/v8/finance/chart/%5ENDX · https://query1.finance.yahoo.com/v8/finance/chart/%5EGSPC (calc_out.txt) |
| 회복 15년 7개월·7년 2개월 / 3년 2개월·5년 5개월 / 3개월 반·6개월 / 2년 1개월·2년 / 4개월·4개월 | 2015-11-03·2007-05-30 / 2011-01-03·2013-03-28 / 2020-06-05·2020-08-18 / 2023-12-15·2024-01-19 / 2025-06-24·2025-06-27 | S1 https://query1.finance.yahoo.com/v8/finance/chart/%5ENDX · https://query1.finance.yahoo.com/v8/finance/chart/%5EGSPC (calc_out.txt) |
| 1천만원 → 171만원·509만원 | -82.9% · -49.1% | S1 https://query1.finance.yahoo.com/v8/finance/chart/%5ENDX (calc_out.txt) |
| 11월 18일 종가 최고점보다 13.2%·6.3% 아래 | 27,116 / 31,224(10/6) · 7,324 / 7,819(10/6) — 11/19 다시 받음 | S1 https://query1.finance.yahoo.com/v8/finance/chart/%5ENDX · https://query1.finance.yahoo.com/v8/finance/chart/%5EGSPC (calc_out.txt) |
| 10년 5.6배·3.4배 | 5.59 · 3.36 | S1 https://query1.finance.yahoo.com/v8/finance/chart/%5ENDX · https://query1.finance.yahoo.com/v8/finance/chart/%5EGSPC (calc_out.txt) |
| 1985년 10월부터 242배·40배 | 241.8 · 39.6 (11/19 다시 받음) | S1 https://query1.finance.yahoo.com/v8/finance/chart/%5ENDX · https://query1.finance.yahoo.com/v8/finance/chart/%5EGSPC (calc_out.txt) |
| 매달 적립 2001년 10월 51% 손실, 2004년 12월 본전, 2009년 3월 31% 아래, 8월 회복 | -50.6% · 2004-12-01 · -31.1% · 2009-08-03 | S1 https://query1.finance.yahoo.com/v8/finance/chart/%5ENDX (calc_out.txt) |
| 2008년은 주택담보대출 부실이 은행·금융시장을 흔든 위기 | 'losses on mortgage-related financial assets began to cause strains in global financial markets' | S3 https://www.federalreservehistory.org/essays/great-recession-and-its-aftermath |
| (H) = 환율 변동을 막아 둔 환헤지형 | '환헤지형으로서 원달러 환율변동율을 헤지' | S4 https://investments.miraeasset.com/tigeretf/ko/product/search/detail/index.do?ksdFund=KR7448300004 |

# 올리기 전 확인
- 2026-11-19 22:43 firemap-write-b(발행 날 다시 확인)
- 다시 연 주소: https://query1.finance.yahoo.com/v8/finance/chart/%5ENDX · https://query1.finance.yahoo.com/v8/finance/chart/%5EGSPC (다시 받아 calc.py 다시 돌림, 11/18 받은 것 raw/1118/) · https://indexes.nasdaqomx.com/docs/Methodology_NDX.pdf (200, 'non-financial companies' 그대로 — raw/1118/ndx_method_1119.pdf) · https://www.federalreservehistory.org/essays/great-recession-and-its-aftermath (200) · https://investments.miraeasset.com/tigeretf/ko/product/search/detail/index.do?ksdFund=KR7448300004 (200, '환헤지형' 문구 그대로) · S5 etfshopping(2차, 대조 칸에 안 씀)은 429로 못 엶
- 기준일: Yahoo ^NDX·^GSPC 2026-11-18 종가(11/19 22:43 받음 — 11/19 미국 장은 아직 열리기 전)
- 바뀐 것: 최고점 대비 나스닥100 13.5→13.2%(27,002→27,116), S&P500 6.1→6.3%(7,341→7,324) · 전체 나스닥100 240.8→241.8배(글 241→242배) · 10년 5.6·3.4배와 하락장 다섯 번 낙폭·회복·적립 숫자는 그대로 · c00·c03·c05 날짜 11월 17일→18일, 출처 '11월 19일 받음', 01.png 기간 줄
- 새로 찾은 것: 10/6 최고점은 11/18까지 그대로(새 최고점 없음)
- 2026-11-18 17:03 firemap-write-b(조사·작성 날, 발행 전날 — 발행 회차가 11/19 다시 열 것)
- 다시 연 주소: https://query1.finance.yahoo.com/v8/finance/chart/%5ENDX · https://query1.finance.yahoo.com/v8/finance/chart/%5EGSPC · https://indexes.nasdaqomx.com/docs/Methodology_NDX.pdf · https://www.federalreservehistory.org/essays/great-recession-and-its-aftermath · https://investments.miraeasset.com/tigeretf/ko/product/search/detail/index.do?ksdFund=KR7448300004 · https://etfshopping.com/lab/hedged-vs-unhedged
- 기준일: Yahoo ^NDX·^GSPC 2026-11-17 종가(11/18 16:51 받음)
- 바뀐 것: 처음 조사 — 없음
- 새로 찾은 것: 하락장 다섯 번 중 S&P500이 더 빠진 두 번(2008·2020) · 나스닥100 매달 적립 본전 2004년 12월 · 10/6 최고점 대비 13.5%·6.1%
- 조사 뒤 공표: data/release_calendar.json 확인 필요 — 발행 날(11/19) 회차가 raw 다시 받아 calc.py 다시 돌리고 c03·c05의 '11월 17일 종가'·13.5%·6.1%를 최신 종가로 바꾼다(지수 글 시효 = 미국 장 마감)

# 교차검증 (crosscheck 11/18 17:01, gemini-3.8-flash 사실·말투 — OpenAI 키 없음)
- 사실 지적 5건: 반영 2 · 유지 3 — ① 기간 연도 빠짐 → '자료가 시작된 1985년 10월부터 올해 11월 17일까지' ② '지난달 최고점' 날짜 빠짐 → '두 지수 모두 10월 6일에 최고점' ③ '배당까지 더하면 수익이 커짐' 유지(배당은 0 이상이라 총수익 ≥ 가격 수익, 경쟁 3·5위 총수익 연 15.3·20.9%가 우리 가격 연 12.9·18.8%보다 큼) ④ 'ETF는 보수·세금 때문에 지수와 다름' 유지(S4 운용사 상품 정보에 총보수 칸) ⑤ '다음 하락장은 알 수 없음' 유지(예측하지 않는다는 사실 문장, 권유 방지)
- 말투 11건: 반영 10(고친 문장 그대로, 날짜가 낡는 '어제'만 '11월 17일'로) · 유지 1(끝 질문 — 뒤에 이해 시험 2차에서 ㉢ 게시판 안내로 바꿈)
- 이해 시험 1~2차 반영 뒤 readcheck 0 · aitell 1.1 · spoken 통과 · selfcheck 사실 0
