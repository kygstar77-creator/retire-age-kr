# tigersp1121 자료조사 (카페 11/21 12:40 지수 칸 — firemap-write 11/20 07:10 회차) — 지수투자 장르, 계산 사례형(직접 계산)

## 검증
- 범위: 사장님 11/19 '배당·지수·부동산' 중 ② 지수투자 — S&P500 지수 ETF(TIGER 미국S&P500) 매달 나눠 사기 vs 한 번에, 실제 종가로 직접 계산(개별주·시황·전망 아님, 사라·팔라 없음). 세금은 '세전·안내 한 줄'
- 수요: kwvol 11/20 07:1x — TIGER미국S&P500 102,000 · S&P500ETF 17,300 · TIGER미국나스닥100 27,220 · S&P500적립식 30(검색어 아님 → 제목은 상품 이름 앞)
- 경쟁: toprank 'TIGER 미국S&P500 적립식'·'S&P500 적립식 5년 수익률' 상위 16 중 7편 읽음(bench.md) — 연 3~10% 가정 계산 4편·달러 지수 1편·투자일기, 원화 실제 종가로 매달 산 5년 결과를 센 글 0편
- 겹침: 우리 S&P500 글 #413(분배금 KODEX 두 배)·#422(보수 싼 게 수익률)·블로그 tigersp(1년 환율) — 이번은 적립식 vs 한 번에. 코스피200 적립식(#416)과 지수 다름. 11/21 칸: 07:40 부동산·10:10 배당·12:40 이 글(S&P500)·16:10 부동산·18:40 지수 둘째(다른 지수)·22:40 배당 짝 글

## 원문
- S1 미래에셋자산운용 TIGER 미국S&P500 상품 페이지(기초지수 S&P 500 Index 원화환산·환헤지 하지 아니함·총보수 연 0.0068%·상장 2020-08-07·세금 안내 15.4%), 11/20 07:1x 받음(raw/tiger_detail_full.txt): https://investments.miraeasset.com/tigeretf/ko/product/search/detail/index.do?ksdFund=KR7360750004
- S2 미래에셋자산운용 TIGER 연도별 분배금(360750 주당 2026 253·2025 243·2024 253·2023 200·2022 160원), 11/20 07:1x 받음(raw/tiger_annual_sp.txt): https://investments.miraeasset.com/tigeretf/ko/distribution/annual/list.do
- S3 (2차) 야후 파이낸스 360750.KS 일별 종가·분배 events, 11/20 07:14 받음(raw/y_360750.KS.json): https://query1.finance.yahoo.com/v8/finance/chart/360750.KS?range=10y&interval=1d&events=div
- S4 (2차) 네이버 fchart 360750 일별(분배금 수정주가 — 최근 3일 종가 대조용), 11/20 07:2x 받음(raw/nvf_360750.xml): https://fchart.stock.naver.com/sise.nhn?symbol=360750&timeframe=day&count=1400&requestType=0
- S5 같은 자료로 직접 계산(calc.py → calc_out.txt·series.json) — 원자료 S2·S3, 대조 S1·S4

## 경쟁
- toprank.txt('TIGER 미국S&P500 적립식' 상위 8)·toprank_q1.txt('S&P500 적립식 5년 수익률' 상위 8). 읽은 7편은 bench.md.

## 질문
1. S&P500 ETF에 매달 50만원 넣으면 얼마가 될까 — https://blog.naver.com/ttajeobom/224478091776 (연 7% 가정으로만 계산) → 답: 실제 TIGER 미국S&P500 종가로 2021년 12월부터 60번이면 3,000만원 → 약 4,353만원(분배금 약 112만원 포함, 세전)
2. 매달 나눠 사는 것과 한 번에 넣는 것 중 뭐가 나은가 — https://blog.naver.com/ckskck123/224482194081 (달러 지수로 전략 비교) → 답: 이 5년은 한 번에 넣은 쪽이 약 5,571만원으로 약 1,218만원 많음, 대신 2022년 6월 바닥에서 손해는 약 363만원 vs 약 40만원
3. S&P500 적립 60개월 실제 결과는 — https://blog.naver.com/winnerking/224470663135 ('실제 수익률을 확인하지 못해 칸을 비워 둠') → 답: 60번 실제 종가·분배금 20번으로 채움
4. 원화로 사면 환율 때문에 달라지나 — https://blog.naver.com/edgar617/224435111487 → 답: TIGER 미국S&P500은 환헤지를 하지 않아 환율이 바뀌면 값이 같이 움직임(S1), 이 글 숫자는 원화 종가라 환율이 이미 들어 있음

## 왜
- 왜 한 번에 산 쪽이 많나: 첫 달 종가 13,700원 뒤 값이 대체로 올라 나중 돈일수록 비싸게 삼 — 매달 평균 단가 약 17,260원, 같은 돈으로 451주 차이(S5)
- 왜 매달 쪽 바닥 손해가 작나: 2022년 6월 17일까지 350만원만 넣은 상태(S5)
- 왜 7월 뒤 금액이 줄었나: 종가 28,875원 → 24,400원(15.5% 낮음), 넣은 돈이 쌓인 뒤라 금액 변화가 큼(S3·S5) — 값이 왜 내렸는지는 자료에 없어 안 씀

## 그래서
- 결과만 보면 이 5년은 한 번에 넣은 쪽이 많았고, 나눠 산 쪽은 초반 하락 때 손해가 작았음 — 어느 쪽을 고를지는 독자 몫(권유 없음)
- 세금은 계좌(일반·연금저축·ISA)에 따라 다름 — 일반 계좌 15.4%는 미래에셋 안내 원문으로 확인
- 분배금 기록은 미래에셋 연도별 분배금 페이지에서 확인

## 누구라면
- 월급에서 매달 넣는 사람: 3,000만원 → 약 4,353만원, 2022~2023년 초 10번 손해였다가 그 뒤엔 없음
- 목돈이 있는 사람: 3,000만원 → 약 5,571만원, 대신 2022년 6월엔 약 363만원 손해
- 7월 고점 근처에 시작한 사람: 그 뒤 15.5% 낮은 가격 — 이 글은 2021년 12월 시작만 셈

## 함정
- 가정 수익률(연 7% 등) 계산을 실제 결과로 읽음
- '적립식이 늘 낫다'로 읽음 — 이 5년은 반대
- 세전 숫자를 손에 쥔 돈으로 읽음

## 한계
- 시작 달 하나(2021년 12월)·매달 첫 거래일 종가만 — 다른 날 시작하면 결과가 다름
- 세금·매매 수수료 안 넣음(총보수는 따로 빼지 않음)
- 분배금은 받은 돈으로만 셈(재투자 안 함), 분배락 날(야후 events 날짜) 전 보유 주식 기준
- 2022년 7월 분배금은 야후에 없어 미래에셋 2022 합계 160원 - 야후 120원 = 40원으로 채움(날짜 2022-07-28로 둠)
- 종가는 야후 원래 종가 — 네이버 일별은 분배금 반영 수정주가라 옛 날짜 값이 다름, 최근 3일은 같음

## 대조
| 글 값 | 원문 값 | 출처 |
|---|---|---|
| 매달 50만원 60번, 넣은 돈 3,000만원 → 약 4,353만원 | 60번 · 30,000,000 · 43,534,955 | S3 https://query1.finance.yahoo.com/v8/finance/chart/360750.KS?range=10y&interval=1d&events=div · S5 calc_out.txt |
| 분배금 약 112만원(매달), 약 229만원(한 번에) | 1,121,385 · 2,285,316 | S2 https://investments.miraeasset.com/tigeretf/ko/distribution/annual/list.do · S3 · S5 |
| 한 번에 약 5,571만원, 약 1,218만원 많음 | 55,707,616 · 12,172,661 | S3 · S5 calc_out.txt |
| 첫 달 종가 13,700원, 2,189주 | 2021-12-01 13700 · 2,189주 | S3 https://query1.finance.yahoo.com/v8/finance/chart/360750.KS?range=10y&interval=1d&events=div |
| 1,738주, 평균 단가 약 17,260원, 451주 차이 | 1,738 · 17,258 · 451 | S5 calc_out.txt |
| 2022년 6월 17일 11,960원, 약 2,637만원·363만원 손해, 350만원 → 약 310만원·40만원 손해 | 11960 · 26,366,260 · 3,633,740 · 3,095,200 · 404,800 | S3 https://query1.finance.yahoo.com/v8/finance/chart/360750.KS?range=10y&interval=1d&events=div · S5 |
| 넣은 돈과 비교하면 둘 다 12%쯤 빠짐 | -11.57% · -12.11% | S5 calc_out.txt |
| 산 날 60번 중 10번, 2022년 2월~2023년 3월 | 10/60 · 20220203~20230302 | S5 calc_out.txt |
| 7월 2일 28,875원, 24,400원은 15.5% 낮음 | 28875 · 24400 · -15.5% | S3 https://query1.finance.yahoo.com/v8/finance/chart/360750.KS?range=10y&interval=1d&events=div · S4 https://fchart.stock.naver.com/sise.nhn?symbol=360750&timeframe=day&count=1400&requestType=0 |
| 7월 2일 2,800만원 → 약 4,888만원, 200만원 더 | 28,000,000 · 48,880,439 | S5 calc_out.txt |
| 한 번에 쪽 7월 2일 약 6,523만원 | 65,227,577 | S5 calc_out.txt |
| 분배금 1년에 네 번 | 2022~2026 해마다 4번 | S3 https://query1.finance.yahoo.com/v8/finance/chart/360750.KS?range=10y&interval=1d&events=div · S2 |
| 2026년 11월 19일 종가 24,400원 | 24,400 | S1 https://investments.miraeasset.com/tigeretf/ko/product/search/detail/index.do?ksdFund=KR7360750004 · S3 · S4 |
| 분배금 20번 | 2022~2026 연 4번, 주당 합 1,109원 | S2 https://investments.miraeasset.com/tigeretf/ko/distribution/annual/list.do · S3 |
| 2022년 7월 40원, 2022년 합계 160원 | 160 - 120 = 40 | S2 https://investments.miraeasset.com/tigeretf/ko/distribution/annual/list.do · S3 |
| 배당소득세 15.4% | '분배금은 배당소득세 과세 : Min(현금분배금, 과표증분) X 15.4%' | S1 https://investments.miraeasset.com/tigeretf/ko/product/search/detail/index.do?ksdFund=KR7360750004 |
| 환율 변동을 막아 두지 않음, S&P500 원화 환산 | 환헤지 사항 '환헤지를 하지 아니함' · 'S&P 500 Index(원화환산)' | S1 https://investments.miraeasset.com/tigeretf/ko/product/search/detail/index.do?ksdFund=KR7360750004 |

# 올리기 전 확인
- 2026-11-20 07:2x firemap-write(조사·작성 날 = 발행 전날, 발행 11/21 12:40 — 1일 안)
- 다시 연 주소: https://investments.miraeasset.com/tigeretf/ko/product/search/detail/index.do?ksdFund=KR7360750004 · https://investments.miraeasset.com/tigeretf/ko/distribution/annual/list.do · https://query1.finance.yahoo.com/v8/finance/chart/360750.KS?range=10y&interval=1d&events=div · https://fchart.stock.naver.com/sise.nhn?symbol=360750&timeframe=day&count=1400&requestType=0 · 경쟁·질문 글 https://blog.naver.com/ttajeobom/224478091776 · https://blog.naver.com/ckskck123/224482194081 · https://blog.naver.com/winnerking/224470663135 · https://blog.naver.com/edgar617/224435111487 (bench_fetch.py) (11/20 07:1x~07:2x)
- 기준일: 2026-11-19 종가(국내 장 마감 15:30 뒤)
- 바뀐 것: 처음 조사 — 없음(최근 분배금 2026-10-30 기준 주당 60원, 다음 분배 2027-01 말 미발표)
- 새로 찾은 것: 원화 실제 종가로 매달 50만원 5년 — 약 4,353만원 vs 한 번에 약 5,571만원, 바닥 손해 40만 vs 363만원 · 경쟁 16편 0편
- 조사 뒤 공표: data/release_calendar.json 해당 없음 — 11/20 장 마감 뒤 종가가 바뀜 → 발행 날(11/21) 아침 11/20 종가로 숫자 갱신 후 재서명
