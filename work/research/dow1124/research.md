# dow1124 자료조사 (카페 11/24 10:10 칸, firemap-write 11/22 23:1x 회차 — 운영실장 23:10 지시) — 다우지수 주가 가중, 원문 정리+직접 계산형

## 검증
- 수요: kwvol 11/22 — 다우지수 631,600(PC 13,800·모바일 617,800, 시세 보러 오는 검색이 많음) · 나스닥다우지수 307,210 · VT 5,980 · ACWI 60 · 전세계ETF 15
- 경쟁에서 터진 증거: toprank '다우지수 계산 방법' 상위 8편 중 1·2위가 11/22, 나머지 2일~3주 안 — 요즘 계속 쓰이는 주제
- 겹침: 11/24 07:40 tigerdj1122(미국배당다우존스 — 다른 지수)·16:10 rsp1124(S&P500 동일가중 수익 비교)·11:30 KOSPI-1(코스피 급락)과 다른 각도(지수 계산 방식·비중) · 우리 카페 다우지수 글 0편 · 11/22 spx10y·ndxetf와 축(지수)만 같고 대상 다름
- 축 배분: 11/24 배당(07:40)→지수(10:10 이 글)→부동산(12:40)→지수(16:10)→?(18:40)→배당(22:40) — 같은 축 3칸 연속 없음

## 원문
- S1 State Street DIA 보유 종목 파일 As of 19-Nov-2026(30종목, 주식 수 모두 5,262,145, 비중), 11/22 받음(raw/dia_holdings.xlsx): https://www.ssga.com/us/en/intermediary/library-content/products/fund-data/etfs/us/holdings-daily-us-en-dia.xlsx
- S2 State Street SPY 보유 종목 파일 As of 19-Nov-2026, 11/22 받음(raw/spy_holdings.xlsx): https://www.ssga.com/us/en/intermediary/library-content/products/fund-data/etfs/us/holdings-daily-us-en-spy.xlsx
- S3 State Street DIA 상품 페이지(Gross Expense Ratio 0.16%·Inception Jan 14 1998·"price-weighted index of 30 component common stocks"), 11/22 받음(raw/ssga_dia.txt): https://www.ssga.com/us/en/intermediary/etfs/state-street-spdr-dow-jones-industrial-average-etf-trust-dia
- S4 야후 파이낸스 chart API 30종목·^DJI 11/19 종가, ^DJI·^GSPC 2년 일별, 11/22 받음(raw/): https://query1.finance.yahoo.com/v8/finance/chart/%5EDJI · https://query1.finance.yahoo.com/v8/finance/chart/%5EGSPC
- S5 S1·S4로 직접 계산(calc.py → calc_out.txt)
- S6 Invesco RSP 상품 페이지 "the market-cap-weighted S&P 500 Index"(rsp1124가 11/22 받은 파일 raw/invesco_rsp_1122.txt): https://www.invesco.com/us/en/etf/sp-500-equal-weight-rsp.html

## 경쟁
- toprank.txt('다우지수 계산 방법' 블로그 상위 8, 11/22). 본문 5편 bench_raw. 1(joaijoa1) 주가 가중 원리·제수 0.12 가정 예시, 2(rachel57942) 30종목 구성·업종 배분, 3(mike1353) 세 지수 차이, 4(awesomekim83) 구성 기업·계산식, 6(dlfdjdl) 세 지수 표. 실제 11/19 비중·1달러당 포인트·같은 회사 S&P500 비중과 맞댄 글 0편 → bench.md

## 질문
1. 다우는 왜 비싼 주식 비중이 큰가 — https://blog.naver.com/joaijoa1/224473009068 ('주가 비싼 종목이 높은 비중을 차지하는 이유') → 답: 30종목을 같은 주식 수(526만 2,145주)로 담음, 1주 값이 비중
2. 다우·나스닥·S&P500 차이가 뭔가 — https://blog.naver.com/mike1353/224480798676 ('나스닥·S&P500·다우 차이') → 답: 같은 회사도 다우 비중과 S&P500 비중이 뒤집힘(GS 9.6% vs 0.4%, NVDA 1.8% vs 6.0%)
3. 다우 몇 포인트 하락이 얼마나 큰가 — https://blog.naver.com/awesomekim83/224464225519 ('다우는 어떻게 계산하나요?') → 답: 1달러 = 약 5.94포인트, GS 5% = 240포인트, NVDA 5% = 46포인트
4. 다우 30종목만으로 시장 전체를 보여 주나 — https://blog.naver.com/rachel57942/224472993939 ('미국 증시 전체를 설명하기에 부족한 부분') → 답: 30종목은 S&P500 안에서 39.1%, 1년 가격 등락 다우 6.5% vs 6.2%

## 왜
- 왜 GS가 1위인가: 주식 수가 같아 1주 값(847.53달러)이 30종목 중 가장 비쌈(S1·S4) — 원문(S3) "price-weighted"
- 왜 1달러가 5.94포인트인가: 지수 = 주가 합 ÷ 제수, 계산한 제수 0.168248(S5) — 제수 공식 값은 방법론 PDF 403이라 못 봄
- 왜 제수가 바뀌나(액면분할): 원문 방법론을 못 열어 '주식을 쪼개면 1주 값이 낮아져 비중이 준다'까지만 씀

## 그래서
- 다우 몇백 포인트 뉴스는 비싼 종목 몇 개가 크게 움직였을 수 있음 — 종목별 1달러 = 같은 포인트
- 미국 대형주 전체 흐름은 S&P500, 다우는 30종목 가격 합으로 따로 읽음
- 다우를 사는 ETF(DIA)는 보수 연 0.16%(본문엔 안 넣음 — 이해 시험 1차 3명이 상품 소개처럼 읽음)

## 누구라면
- 뉴스로 미국 증시만 보는 사람: '다우 하락 = 내 S&P500 ETF 하락'이 아님 — 비중이 다름
- 엔비디아·애플 비중 때문에 지수 ETF를 고르는 사람: 다우에선 두 회사 비중이 작음(1.8%·4.2%)
- 이미 S&P500 ETF를 가진 사람: 다우 30종목이 그 안에 39.1% 들어 있음

## 함정
- '다우 = 미국 대표 30대 기업 시가총액 순'이라는 오해 — 비중 1위는 시총이 아니라 주가(골드만삭스)
- 같은 5% 상승이라도 지수 영향은 5배 넘게 차이(240 vs 46포인트)
- 액면분할하면 같은 회사라도 다우 비중이 줆

## 한계
- 제수는 S&P 다우존스 지수 공식 값이 아니라 종가 합 ÷ 지수로 계산한 값(방법론 PDF 403) — DIA 비중과 0.05%p 안에서 맞아 그대로 씀
- 1년 등락은 가격 지수(배당 뺌)·달러 기준
- 보유 종목은 11/19 하루 값 — 주가 따라 매일 바뀜
- 국내 상장 다우 ETF는 이번에 안 봄

## 대조
| 글 값 | 원문 값 | 출처 |
|---|---|---|
| 30종목 같은 주식 수 523만 2,475주 | Shares Held 5,232,475(30줄 같음, 11/24) | S1 https://www.ssga.com/us/en/intermediary/library-content/products/fund-data/etfs/us/holdings-daily-us-en-dia.xlsx |
| 골드만삭스 9.6% · 엔비디아 1.8% · 나이키 0.4% · 캐터필러 6.4% · 마이크로소프트 5.9% · 애플 4.2% · 아마존 3.0% | 9.571 · 1.845 · 0.42 · 6.419 · 5.891 · 4.2 · 3.0(11/24) | S1 https://www.ssga.com/us/en/intermediary/library-content/products/fund-data/etfs/us/holdings-daily-us-en-dia.xlsx |
| S&P500 골드만삭스 0.4% · 캐터필러 0.4% · 마이크로소프트 5.9% · 애플 8.3% · 아마존 4.0% · 엔비디아 6.0% | 0.38 · 0.40 · 5.92 · 8.31 · 3.98 · 6.05(11/24) | S2 https://www.ssga.com/us/en/intermediary/library-content/products/fund-data/etfs/us/holdings-daily-us-en-spy.xlsx |
| 다우 30종목 S&P500 안 비중 합 39.1% · 상위 5곳 중 S&P500 상위 10위는 마이크로소프트 하나 | 39.1 · MSFT만 | S2·S5 calc_out.txt https://www.ssga.com/us/en/intermediary/library-content/products/fund-data/etfs/us/holdings-daily-us-en-spy.xlsx |
| S&P500은 회사 덩치(시가총액)만큼 담음 · 500여 곳 | "market-cap-weighted S&P 500 Index" · SPY 종목 줄 504 | S6 https://www.invesco.com/us/en/etf/sp-500-equal-weight-rsp.html · S2 |
| 주가 가중 지수 | "price-weighted index of 30 component common stocks" | S3 https://www.ssga.com/us/en/intermediary/etfs/state-street-spdr-dow-jones-industrial-average-etf-trust-dia |
| DIA 보수 연 0.16% | Gross Expense Ratio 0.16% | S3 https://www.ssga.com/us/en/intermediary/etfs/state-street-spdr-dow-jones-industrial-average-etf-trust-dia |
| 1주 약 806달러 · 155달러 · 36달러 | 806.02 · 155.38 · 35.75(11/24) | S4 https://query1.finance.yahoo.com/v8/finance/chart/GS |
| 30종목 종가 합 8,416달러 · 다우 5만 19포인트 · 1달러 = 약 5.94포인트 | 8,415.56 · 50,018.7 · 1÷0.168248 = 5.94 | S4·S5 calc_out.txt https://query1.finance.yahoo.com/v8/finance/chart/%5EDJI |
| 5% 상승 GS 240 · MSFT 147 · NVDA 46포인트 · 5배 넘게 | 240 · 147 · 46 · 5.2 | S5 calc_out.txt https://query1.finance.yahoo.com/v8/finance/chart/%5EDJI |
| 상위 5곳 합 32.5% | 32.5 | S1·S5 https://www.ssga.com/us/en/intermediary/library-content/products/fund-data/etfs/us/holdings-daily-us-en-dia.xlsx |
| 1년 다우 6.5% · S&P500 6.2%(11/25 종가) | +6.5 · +6.2 | S4·S5 https://query1.finance.yahoo.com/v8/finance/chart/%5EGSPC |

# 올리기 전 확인
- 2026-11-27 09:4x firemap-write(발행 날) — DIA·SPY 보유 파일·야후 30종목·^DJI·^GSPC 다시 받아 calc.py(D=11/24) 다시 돌림
- 다시 연 주소: https://www.ssga.com/us/en/intermediary/library-content/products/fund-data/etfs/us/holdings-daily-us-en-dia.xlsx · https://www.ssga.com/us/en/intermediary/library-content/products/fund-data/etfs/us/holdings-daily-us-en-spy.xlsx · https://www.ssga.com/us/en/intermediary/etfs/state-street-spdr-dow-jones-industrial-average-etf-trust-dia · https://www.invesco.com/us/en/etf/sp-500-equal-weight-rsp.html · https://query1.finance.yahoo.com/v8/finance/chart/GS · https://query1.finance.yahoo.com/v8/finance/chart/%5EDJI · https://query1.finance.yahoo.com/v8/finance/chart/%5EGSPC
- 기준일: 2026-11-24 보유 종목·종가 · 1년 등락 2026-11-25 종가(11/26 휴장)
- 바뀐 것: 11/19→11/24 — GS 10.3→9.6%·NVDA 1.8% 그대로(S&P500 5.7→6.0%)·1주 GS 848→806·NVDA 146→155달러·주식 수 526만 2,145→523만 2,475주·5% 상승 GS 252→240·NVDA 43→46포인트(6배 가까이→5배 넘게)·상위 5곳 32.9→32.5%·S&P500 안 다우 30종목 38.5→39.1%·1년 다우 5.2→6.5%·S&P500 5.7→6.2%(이제 다우가 앞섬)·1달러 5.94포인트 그대로 · 본문·그림 3장 모두 고침
- 새로 찾은 것: 닷새 사이 GS 주가가 5% 빠지며 비중 0.7%p 줄었는데 순서(1위 GS·꼴찌 NKE)는 그대로 · 1년 등락 순서가 뒤집힘(다우 6.5% > S&P500 6.2%)
- 조사 뒤 공표: data/release_calendar.json — 보유 종목 매일 갱신, 다우 구성 종목 변경 공지 11/22 뒤 없음(확인 안 함 — S&P DJI 공지 페이지 403)
