# sp500etf1114 자료조사 (카페 2026-11-14 10:10 칸 — firemap-write-b 11/13 16:4x) — 배당ETF·지수 축: 국내 S&P500 ETF 5개 수익률·실부담비용

## 검증
- 수요: work/kwvol.py 11/12 잰 값 — TIGER미국S&P500 105,500 · S&P500ETF 18,320 (운영실장 15:10 배차 근거, slots.json)
- 겹침: 우리 카페 spvs0929(#161, TIGER vs KODEX 두 개 수익)·sp500dist1112(#413, 분배금 차이) — 5개 3·5년 수익률과 실부담비용 각도는 처음
- 경쟁에서 터진 증거: toprank 'S&P500 ETF 비교' 블로그 상위 8편 중 7편이 11/5~11/13 작성, 댓글 20(tkos3333)·12(awxs2_) · 배투모 주간 인기글 '나스닥 S&P500 5년이상 투자하신분들 수익률 공유' 조회 3,560·댓글 31(11/13 API)

## 원문
- S1 FunETF 상품 정보 5개 — 2026-11-13 확인(raw/funetf_*.txt, 11/12 기준값): https://www.funetf.co.kr/product/etf/view/KR7360750004 · https://www.funetf.co.kr/product/etf/view/KR7379800008 · https://www.funetf.co.kr/product/etf/view/KR7360200000 · https://www.funetf.co.kr/product/etf/view/KR7379780002 · https://www.funetf.co.kr/product/etf/view/KR7433330002 (2차 — 모음 사이트)
- S2 삼성자산운용 KODEX 미국S&P500 상품 API — 2026-11-13 확인(raw/kodex_2ETFE4.json): https://m.samsungfund.com/api/v1/kodex/product/2ETFE4.do
- S3 한국투자신탁운용 ACE 미국S&P500 API — 2026-11-13 확인(raw/ace.json): https://papi.aceetf.co.kr/api/funds/K55101D78195
- S4 미래에셋 TIGER 미국S&P500 상품 페이지 — 2026-11-13 확인(raw/tiger.txt): https://investments.miraeasset.com/tigeretf/ko/product/search/detail/index.do?ksdFund=KR7360750004
- S5 네이버페이 증권 ETF 정보 — 2026-11-13 확인(raw/naver_*.json): https://m.stock.naver.com/api/stock/379780/integration · https://m.stock.naver.com/api/stock/433330/integration · https://m.stock.naver.com/api/stock/360750/integration (2차)
- S6 KB자산운용 'ETF 비용은 총보수만 보면 될까?' — 2026-11-13 확인(raw/kbam_cost.txt): https://kbam.co.kr/insights/guide/etf-total-expense-ratio-vs-actual-cost
- S7 삼성자산운용 공지 '삼성 KODEX 미국대표지수 ETF 분배금 지급 정책 안내'(2025.5.7) — 2026-11-12 확인: https://www.samsungfund.com/etf/lounge/notice-view.do?no=66913
- S8 소득세법 제129조 100분의 14 — 2026-11-12 확인: https://www.law.go.kr/법령/소득세법/제129조
- S9 야후 파이낸스 일별 종가·분배 — 2026-11-13 확인(raw/yahoo_*.json, 대조용): https://query1.finance.yahoo.com/v8/finance/chart/360750.KS?range=5y&interval=1d&events=div

## 경쟁
- bench.md 참조. 1위(protectmoney 11/13)는 세 상품 1년 수익률·TIGER 합성총보수 한 시점, 5위(fallinloverich)는 ACE·TIGER 실비용 표, 6위(tkos3333)는 개인 계좌 수익률. 다섯 개 3년·5년 수익률을 나란히 놓고 실부담비용 순위와 맞댄 글 0편

## 질문
1. 같은 지수인데 아무거나 사도 될까 — https://blog.naver.com/fallinloverich/224474776959 (5위 본문 첫 물음) → 답: c00·c01(3년 0.73%p, 1억원 약 73만원)
2. 5년 넘게 투자하면 수익률이 얼마나 되나 — https://cafe.naver.com/ca-fe/cafes/31050378/articles/67956 (배투모 주간 인기 조회 3,560·댓글 31) → 답: c01(5년 93.69~94.93%)
3. 수수료(총보수) 가장 낮은 ETF가 장기투자에 유리할까 — https://blog.naver.com/protectmoney/224475403569 (1위 '진짜 투자비용은 470원이 전부일까요?') → 답: c02·c03(실부담비용 14~30배, 총보수 순서와 수익률 순서 다름)

## 왜
- 실부담비용이 총보수보다 큰 이유: 기타비용(지수사용료·회계감사비)·매매·중개수수료가 더해짐(S6)
- 수익률에 비용이 이미 빠진 이유: 비용은 따로 청구되지 않고 매일 가격에서 차감(S6), FunETF '수익률에는 실비용이 이미 반영'(S1)
- 실부담비용 2위 KODEX가 3·5년 1위인 이유: 운용사·FunETF 원문에 이유 없음 → 글에 '자료에 그 이유가 따로 나와 있지는 않았어요'
- KODEX 분배금이 큰 이유: 유보 배당을 2029년 1월 기준일까지 나눠 분배(S7)

## 그래서
- 비용 비교는 총보수가 아니라 실부담비용으로(금융투자협회 전자공시·ETF CHECK·운용사 페이지, S6)
- 고를 때 3년·5년·1년 순위가 다르니 한 기간 순위로 정하지 않기(S1)
- 일반 계좌는 분배금마다 15.4% 원천징수 → 표 수익률보다 적게 남음(S8)

## 누구라면
- 새로 사는 사람: 3년 기준 1억원당 차이 약 73만원 — 상품보다 넣는 금액·기간이 더 큼
- 분배금을 생활비로 쓰려는 사람: SOL은 거의 매달, 나머지는 석 달에 한 번꼴(S1·S3·S4)
- 이미 하나를 가진 사람: 3년 차이 0.73%p 안이라 순위만 보고 바꿀 근거는 약함(글에는 권유로 쓰지 않음)

## 함정
- 광고 속 총보수(0.0047%)를 실제 비용으로 읽기 — 실부담비용은 14~30배(S1·S6)
- 1년 순위로 고르기 — 1년 1등 RISE, 3·5년 1등 KODEX(S1)
- 표 수익률을 내 손에 남는 돈으로 읽기 — 분배금 재투자·세전 값(S1·S8)

## 우리만
- 5개 상품 3년·5년·1년 수익률과 실부담비용을 한 자리에 놓고 1억원 차이(73만원)·실부담/총보수 배수(14~30배)·'비용 순위와 수익률 순위가 다름'을 직접 계산(calc.py) — 경쟁 7편 0편(1위는 세 상품 1년만)

## 예외
- 환헤지(H)·커버드콜·레버리지 S&P500 ETF는 다른 상품이라 뺌
- 연금저축·IRP·ISA 세금은 다루지 않음
- 미국 직접 상장 ETF(VOO 등)와 비교 안 함

## 한계
- 3·5년 수익률은 FunETF(2차)와 운용사 API(KODEX·ACE 1차)로 맞댔고, TIGER·RISE·SOL 3년 값은 운용사 원문을 못 받음(TIGER 페이지는 1년·상장 이후만, RISE·SOL 상품 페이지 주소 못 찾음) — FunETF + 야후 직접 계산(순위·차이 크기)으로 대조
- 실부담비율의 산출 시점·기간은 FunETF 페이지에 없음(값만 표시) — 금융투자협회 전자공시 원문은 확인 못 함
- KODEX가 비용이 커도 3·5년 1위인 이유는 원문에 없음
- 야후 종가로 직접 계산한 3년 값(77~78%)은 기준가격 수익률(81~82%)보다 4%p쯤 낮음 — 종가와 기준가 차이·분배 기록 범위 때문으로 보이나 확인 못 함 → 글에는 기준가격 값만 씀

## 대조
| 글 값 | 원문 값 | 출처 |
|---|---|---|
| 3년 차이 0.70%p, 1억원 약 70만원 | 78.52 − 77.82 · 178,520,000 − 177,820,000 (11/13 기준) | S1 · S2 · calc_out.txt |
| KODEX 3년 78.52% | 78.52 (yieldYear3, 11/14 다시 받음) | S2 https://m.samsungfund.com/api/v1/kodex/product/2ETFE4.do |
| SOL 3년 77.82%, 1년 1.60% (2차) | 77.82 · 1.6 | S1 https://www.funetf.co.kr/product/etf/view/KR7433330002 · S9 https://query1.finance.yahoo.com/v8/finance/chart/433330.KS?range=5y&interval=1d&events=div |
| 1억 7,852만원·1억 7,782만원 | 1e8×1.7852 · 1e8×1.7782 | S1 · S2 · calc_out.txt |
| 5년 차이 1.25%p, KODEX 95.13%·TIGER 93.88% (2차) | 95.13 − 93.88 | S2 · S1 https://www.funetf.co.kr/product/etf/view/KR7360750004 · S9 |
| SOL 2022년 6월 상장 (2차) | 2022.06.21 | S1 · S5 https://m.stock.naver.com/api/stock/433330/integration |
| RISE 1년 1.96% (2차) | 1.96 | S1 https://www.funetf.co.kr/product/etf/view/KR7379780002 · S9 https://query1.finance.yahoo.com/v8/finance/chart/379780.KS?range=5y&interval=1d&events=div |
| 총보수 0.01% 안, 1억원 4,700~6,800원 | 0.0047 · 0.0062 · 0.0068 | S3 · S4 · S2 · S5 |
| 실부담비용 약 9만 2천원(ACE)~약 14만 2천원(SOL) (2차) | 0.0922% · 0.1424% | S1 · S6 https://kbam.co.kr/insights/guide/etf-total-expense-ratio-vs-actual-cost |
| 14배~30배 | 0.0939/0.0068=13.8 · 0.1424/0.0047=30.3 | S1 · calc_out.txt |
| 실부담비용 정의·매일 가격에서 빠짐 | '총보수+기타비용+매매중개수수료' · '매일 조금씩 차감돼 수익률에 이미 녹아' | S6 https://kbam.co.kr/insights/guide/etf-total-expense-ratio-vs-actual-cost |
| ACE 3년 4등, KODEX 실부담 2번째·3·5년 1등 | 3년 78.52>78.46>78.09>77.97>77.82 · 실부담 0.1424>0.1067>0.0973>0.0939>0.0922 | S1 · S2 · S3 |
| SOL 순자산 약 2,963억원, TIGER 약 21조 46억원 (2차) | 2,963억 · 210,046억 | S1 · S5 https://m.stock.naver.com/api/stock/360750/integration |
| SOL 거의 매달, 나머지 석 달에 한 번꼴 | SOL 금년 10번·작년 12번 / ACE '지급(매분기)' · TIGER 1·4·7·10월 | S1 · S3 · S4 |
| KODEX 2029년 1월까지 쌓아 둔 분배금 | 유보 배당 15분기 분배 | S7 https://www.samsungfund.com/etf/lounge/notice-view.do?no=66913 |
| 1년 지수 2.10%(원화 기준) | 기초지수 idxYieldYear1 2.10 · '기초지수는 배당금재투자를 가정한 총수익지수' | S2 https://m.samsungfund.com/api/v1/kodex/product/2ETFE4.do · S1 https://www.funetf.co.kr/product/etf/view/KR7379800008 |
| 순자산 = ETF에 모인 돈, TIGER 21조 46억·SOL 2,963억 (2차) | 210,046억 · 2,963억 | S1 · S5 https://m.stock.naver.com/api/stock/433330/integration |
| 15.4% | 100분의 14 + 지방소득세 | S8 https://www.law.go.kr/법령/소득세법/제129조 |

# 올리기 전 확인
- 2026-11-13 16:4x(조사 날, firemap-write-b) S1~S6·S9 받음 — **발행 회차(11/14 10:10 칸)가 S1·S2·S3를 다시 받아 기준일(11/13 기준값으로 바뀌었으면 숫자)을 다시 적기**(수익률은 매일 바뀜)
- 다시 연 주소: https://www.funetf.co.kr/product/etf/view/KR7360750004 · https://www.funetf.co.kr/product/etf/view/KR7379800008 · https://www.funetf.co.kr/product/etf/view/KR7360200000 · https://www.funetf.co.kr/product/etf/view/KR7379780002 · https://www.funetf.co.kr/product/etf/view/KR7433330002 · https://m.samsungfund.com/api/v1/kodex/product/2ETFE4.do · https://papi.aceetf.co.kr/api/funds/K55101D78195 · https://investments.miraeasset.com/tigeretf/ko/product/search/detail/index.do?ksdFund=KR7360750004 · https://m.stock.naver.com/api/stock/379780/integration · https://m.stock.naver.com/api/stock/433330/integration · https://m.stock.naver.com/api/stock/360750/integration · https://query1.finance.yahoo.com/v8/finance/chart/360750.KS?range=5y&interval=1d&events=div · https://query1.finance.yahoo.com/v8/finance/chart/433330.KS?range=5y&interval=1d&events=div · https://query1.finance.yahoo.com/v8/finance/chart/379780.KS?range=5y&interval=1d&events=div · https://kbam.co.kr/insights/guide/etf-total-expense-ratio-vs-actual-cost · https://www.samsungfund.com/etf/lounge/notice-view.do?no=66913 · https://www.law.go.kr/법령/소득세법/제129조
- 기준일: 2026년 11월 12일
- 바뀐 것: 조사 날이라 없음
- 새로 찾은 것: 5개 3년 차이 0.73%p(1억원 73만원)·실부담비용 총보수의 14~30배·비용 순위와 수익률 순위가 다름
- 조사 뒤 공표: data/release_calendar.json에 해당 없음
- 2026-11-14 09:3x(발행 날, firemap-write) S1 다섯 주소·S2·S3 다시 엶(raw/funetf_*.txt 26.11.13 기준 · raw1114_kodex.json · raw1114_ace.json, 11/13 받은 값은 raw1113bak/) · 다시 연 주소: https://www.funetf.co.kr/product/etf/view/KR7360750004 · https://www.funetf.co.kr/product/etf/view/KR7379800008 · https://www.funetf.co.kr/product/etf/view/KR7360200000 · https://www.funetf.co.kr/product/etf/view/KR7379780002 · https://www.funetf.co.kr/product/etf/view/KR7433330002 · https://m.samsungfund.com/api/v1/kodex/product/2ETFE4.do · https://papi.aceetf.co.kr/api/funds/K55101D78195 · S4~S9는 11/13 연 그대로(수익률 아닌 제도·정의·보수)
- 기준일: 2026년 11월 13일
- 바뀐 것: 기준일 11/12→11/13 · 3년 차이 0.73%p→0.70%p(1억원 73만원→70만원) · KODEX 3년 82.29→78.52%·SOL 81.56→77.82% · 5년 1.24→1.25%p(KODEX 95.13·TIGER 93.88) · 1년 RISE 2.05→1.96%·SOL 1.70→1.60% · 지수 1년 2.21→2.10% · 순자산 TIGER 21조 46억·SOL 2,963억 · 순위(3년 KODEX>RISE>TIGER>ACE>SOL, 5년 KODEX 1등·TIGER 꼴찌, 1년 RISE 1등·SOL 꼴찌)·총보수·실부담비율은 그대로 · 그림 01·표지 다시 그림 · ACE 자체 API는 stdDt 20261112 그대로라 FunETF 11/13 값 씀
- 새로 찾은 것: 하루 사이 다섯 개 3년 수익률이 모두 약 3.7%p 내려도(지수 3년 84.12→80.31) 순위와 차이(0.7%p대)는 그대로
- 조사 뒤 공표: data/release_calendar.json에 해당 없음

