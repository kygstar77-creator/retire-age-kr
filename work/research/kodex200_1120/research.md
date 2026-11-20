# kodex200_1120 자료조사 (카페 11/20 16:10 칸 — firemap-write 11/19 23:07 회차) — 지수투자 장르, 통계형(직접 계산)

## 검증
- 범위: 사장님 11/19 '배당·지수·부동산' 중 ② 지수투자 — 코스피200 지수 ETF, 분배금 포함 수익을 지수와 견줌(개별주·시황·전망 아님, 사라·팔라 없음). 세금은 '세전·세금 뺌' 한 줄
- 수요: 슬롯 note 11/19 18:25 — kwvol KODEX200 104,200·코스피200 183,100
- 경쟁: 'KODEX 200 수익률' 블로그 탭 상위 8 중 5편 읽음(bench.md) — 분배금 받은 돈을 1억 실제 주수로 셈 + 지수 대비 %p 0편
- 겹침: 11/13 k200etf1113(한 번에 vs 나눠 사기)·10월 #416 코스피200 적립식 — 이번은 분배금 몫과 지수 대비. 11/20 칸: 07:40 맥쿼리(배당)·10:10 평촌(부동산)·12:40 JEPQ(배당)·16:10 이 글(지수)·18:40 하남(부동산)

## 원문
- S1 삼성자산운용 KODEX 200 분배금 현황(기준일·지급일·주당 금액), 11/19 23:1x 받음: https://m.samsungfund.com/api/v1/kodex/divid-info.do?id=2ETF01 (raw/kodex_divid.json)
- S2 삼성자산운용 KODEX 200 상품 정보(기준가격·종가·지수 수익률 공시, 11/18 기준), 11/19 23:1x 받음: https://m.samsungfund.com/api/v1/kodex/product/2ETF01.do (raw/kodex_prod.json)
- S3 (2차) 야후 파이낸스 069500.KS 일별 종가·분배 events, 11/19 23:1x 받음: https://query1.finance.yahoo.com/v8/finance/chart/069500.KS?range=6y&interval=1d&events=div (raw/y_069500.KS.json)
- S4 (2차) 네이버페이 증권 코스피200 지수 일별(KPI200), 11/19 23:1x 받음: https://api.finance.naver.com/siseJson.naver?symbol=KPI200&requestType=1&startTime=20201101&endTime=20261120&timeframe=day (raw/nv_kpi200.txt)
- S5 같은 자료로 직접 계산(calc.py → calc_out.txt) — 원자료 S1·S3·S4, 대조 S2

## 경쟁
- toprank.txt('KODEX 200 수익률' 상위 8, 'KODEX 200 분배금' 상위 8은 toprank_q1.txt — 커버드콜 글뿐이라 안 씀). 읽은 5편은 bench.md.

## 질문
1. KODEX 200 3년 전 1억 넣었으면 얼마 — https://blog.naver.com/nmnpvv/224461073089 (제목 '3년 전 1억 넣었으면 지금 얼마일까') → 답: 5년 전 1억이면 분배금 포함 약 2억 526만원, 주가만 약 1억 9,518만원
2. 분배금까지 넣으면 지수보다 나은가 — https://blog.naver.com/wisefather1113/224483166753 (분배금 포함 수익률과 주가만 수익률 차이를 다룸) → 답: 5년 105.3% vs 지수 93.4%(11.8%p), 그중 10.1%p가 분배금. 지수에 배당이 안 들어 있어 곧바로 견주면 ETF가 앞서 보임
3. 분배금은 해마다 얼마 — https://blog.naver.com/firelife__90/224468653292 ('분배금은 1년에 4번, 연 1% 안팎') → 답: 1억 기준 해마다 178만~219만원, 5년 1,008만원, 4월이 가장 큼
4. 1년만 보면 — https://blog.naver.com/nmnpvv/224461073089 (1년 수익률도 다룸) → 답: 분배금 포함 36.1% vs 지수 33.9%

## 왜
- 왜 지수와 벌어지나: 지수 수익은 주가만, ETF는 분배금을 현금으로 받음(S1) — 분배금 몫이 5년 10.1%p
- 왜 4월 분배금이 큰가: S1에 금액만 있고 이유 없음 — 본문에 안 씀
- 왜 주가만 본 ETF가 지수보다 1.8%p 높나: 자료에 이유 없음 — 본문에 '이유가 없어서 쓰지 않았다'

## 그래서
- ETF와 지수를 견줄 때는 분배금 포함 여부를 먼저 확인함
- 5년 분배금은 1억에 1,008만원이고 분기마다 새로 정해져 앞으로 약속 아님
- 분배금 기록은 삼성자산운용 KODEX 200 페이지에서 확인

## 누구라면
- 분배금을 쓰는 사람: 5년 105.3%(재투자 안 함)
- 분배금으로 다시 사는 사람: 114.7%
- 주가만 보는 사람: 95.2%, 지수와 1.8%p 차이

## 함정
- 지수 수익률(주가만)과 ETF 분배금 포함 수익률을 곧바로 견줘 ETF가 더 낫다고 읽음
- 5년 숫자를 앞으로 수익으로 읽음
- 세금 전 숫자를 손에 쥔 돈으로 읽음

## 한계
- 두 날짜(2021-11-19·2025-11-20)에 산 경우만 — 다른 날 샀으면 숫자가 다름
- 세금(배당소득세)·수수료·총보수 따로 계산 안 함(종가·분배금은 세전)
- 지수는 네이버 일별 종가(가격지수), 총수익지수(배당 포함)는 안 씀
- 분배금 재투자는 지급일 종가에 소수 주로 산다고 가정(단순화)
- 11/19 종가는 야후·네이버 같은 값, 삼성 공시 수익률은 11/18 기준이라 하루 차이

## 대조
| 글 값 | 원문 값 | 출처 |
|---|---|---|
| 2021년 11월 19일 종가 39,045원, 2,561주 | 39,045 · 1억/39,045 = 2,561주 | S3 https://query1.finance.yahoo.com/v8/finance/chart/069500.KS?range=6y&interval=1d&events=div · S5 calc_out.txt |
| 2026년 11월 20일 종가 76,210원, 지수 755.34 | 76210 · 755.34 | S3 https://query1.finance.yahoo.com/v8/finance/chart/069500.KS?range=6y&interval=1d&events=div · S4 https://api.finance.naver.com/siseJson.naver?symbol=KPI200&requestType=1&startTime=20201101&endTime=20261120&timeframe=day |
| 분배금 20번, 약 1,008만원 | 주당 3,935원 · 10,077,535원 | S1 https://m.samsungfund.com/api/v1/kodex/divid-info.do?id=2ETF01 · S3 events · S5 |
| 5년 분배금 포함 105.3%, 주가만 95.2%, 지수 93.4% | +105.26 · +95.18 · +93.41 | S1·S3·S4·S5 calc_out.txt |
| 지수와 차이 11.8%p 중 분배금 10.1%p | 11.84 · 10.08 | S5 calc_out.txt |
| 해마다 2023 약 178만, 2025 약 219만 | 1,779,895 · 2,189,655 | S1 https://m.samsungfund.com/api/v1/kodex/divid-info.do?id=2ETF01 · S5 |
| 2026년 4월 446원, 1월 80원 | 446 · 80 | S1 https://m.samsungfund.com/api/v1/kodex/divid-info.do?id=2ETF01 |
| 재투자 5년 114.7% | +114.69 (삼성 5년 기준가격 수익률 126.00, 11/18 기준) | S5 · S2 https://m.samsungfund.com/api/v1/kodex/product/2ETF01.do |
| 1년 2025-11-20 종가 56,600원 1,766주, 분배 845원 약 149만원 | 56,600 · 1,766 · 845 · 1,492,270 | S1·S3·S5 |
| 1년 분배금 포함 36.1%, 주가만 34.6%, 지수 33.9% | +36.12 · +34.63 · +33.88 (삼성 11/18 기준 종가 42.29·지수 41.56) | S1·S3·S4·S2 |
| 분배금 1.5%p, 5년 10.1%p | 1.52 · 10.08 | S5 calc_out.txt |

# 올리기 전 확인
- 2026-11-20 15:4x firemap-write(발행 날 다시, 발행 11/20 16:10 — 당일). 끝 날짜를 11/20 마감 종가로 바꿈(calc1120.py → calc1120_out.txt, raw1120/)
- 다시 연 주소: https://m.samsungfund.com/api/v1/kodex/divid-info.do?id=2ETF01 (11/19 23:1x, 분배 공시는 10/30분이 마지막 — 다음은 1월 말) · https://m.samsungfund.com/api/v1/kodex/product/2ETF01.do (11/19) · https://query1.finance.yahoo.com/v8/finance/chart/069500.KS?range=6y&interval=1d&events=div (11/20 15:33) · https://api.finance.naver.com/siseJson.naver?symbol=KPI200&requestType=1&startTime=20201101&endTime=20261120&timeframe=day (11/20 15:33) · https://api.finance.naver.com/siseJson.naver?symbol=069500&requestType=1&startTime=20201101&endTime=20261120&timeframe=day (11/20 15:33)
- 기준일: 2026-11-20 종가(국내 장 마감 15:30 뒤, 069500 76,210원·코스피200 755.34 — 야후는 15:33에 아직 76,215라 끝 날 종가만 네이버 값)
- 바뀐 것: 11/20 하루 KODEX 200 80,630→76,210원(-5.5%) · 5년 분배금 포함 116.6→105.3%, 주가만 106.5→95.2%, 지수 104.7→93.4% · 1년 시작을 2025-11-20(56,600원)으로 → 36.1·34.6·33.9% · 차이 11.8%p·분배금 몫 10.1%p는 그대로 · 분배금 1,008만원 그대로
- 새로 찾은 것: 야후와 네이버 종가가 10/23~10/28 며칠 120원쯤 다름(끝 날만 네이버로 맞춤) — 5년 시작 39,045원은 둘이 같음
- 조사 뒤 공표: data/release_calendar.json — 다음 분배금 2027년 1월 말
