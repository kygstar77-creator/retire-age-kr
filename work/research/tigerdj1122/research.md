# tigerdj1122 자료조사 (카페 11/22 16:10 배당 칸, firemap-write-b 11/21 13:1x 회차) — 국내 상장 vs 미국 직접, 직접 계산형

## 검증
- 수요: kwvol 11/21 — TIGER미국배당다우존스 24,260(후보 9개 중 1위) · SCHD배당금 5,530 · 고배당ETF 3,870 · 월배당ETF 2,950
- 경쟁에서 터진 증거: toprank 'TIGER 미국배당다우존스' 상위 8편 중 5편이 1주 안 글(11/21) · 6위 korjap9633 'SCHD vs TIGER 미국배당다우존스, 40대에게 유리한 ETF는?' 댓글 2 · 1위 economicallyperson '1억 투자하면 매달' 댓글 1
- 겹침: 우리 tigerdiv(#39, 9월 분배 38회 기록)·de1pair1117(#448, 업종 구성 같음 — '분산 안 됨')·schdacct1007(계좌별 미국 세금) — 상장 뒤 실제 총수익을 같은 날 1억으로 맞댄 글 0편 · 11/21 kdiv1121(국내 고배당주)·divbear1121(미국 배당 ETF 하락장)·11/22 22:40 DIVO 짝 글과 종목·각도 다름
- 칸: 11/22 16:10 배당(slots.json, 관문 기한 11/22 10:10)

## 원문
- S1 야후 파이낸스 chart API 일별 종가·분배 events 458730.KS·SCHD·KRW=X, 2023-06-01~2026-11-20, 11/21 13:3x 받음(raw/*_chart_20261121.json, fetch.py): https://query1.finance.yahoo.com/v8/finance/chart/458730.KS
- S2 미래에셋자산운용 TIGER ETF 'ETF 분배금 현황' 연간 분배금 표(2026.11.19 기준) 458730 줄, 11/21 받음(raw/tiger_dist_page_1121.txt, fetch_tiger3.py): https://investments.miraeasset.com/tigeretf/ko/product/search/detail/index.do?ksdFund=KR7458730008
- S3 (2차①) 네이버페이 증권 ETF 분석 458730 — 기간 수익률·분배 TTM·총보수·환헤지·기초지수, 11/21 받음(raw/naver_etfan_458730_1121.json): https://m.stock.naver.com/api/stock/458730/etfAnalysis
- S4 미국 국세청 Tax Treaty Table 1(Rev. May 2023) Korea, South 배당 15%, 11/21 받음(raw/irs_treaty_table1_1121.txt): https://www.irs.gov/pub/irs-lbi/tax-treaty-table-1.pdf
- S5 (2차②) FRED DEXKOUS 원달러 일별(apis.fred, 11/21 받음 raw/fred_DEXKOUS_20261121.json): https://fred.stlouisfed.org/series/DEXKOUS
- S6 S1·S2로 직접 계산(calc.py → calc_out.txt) — 원자료 S1, 분배 합 S2와 대조, 기간 수익률 S3과 대조
- S8 (2차③) FunETF 458730 상품 페이지 '총보수 0.0100%, 합성총보수 0.0600%, 실부담비용 0.1058%', 2026-11-22 받음(raw/funetf_458730_1122.html) — 미래에셋 상세 페이지는 headless에서 총보수 칸이 빈 값(raw/tiger_page_1122.txt, fetch_tiger5.py), 운용사 2023-07-19 0.03→0.01% 인하 발표는 매체 기사로만 봄: https://www.funetf.co.kr/product/etf/view/KR7458730009
- S7 찰스 슈왑 SCHD 총보수 0.06%(de1pair1117 research.md 11/19 확인): https://www.schwabassetmanagement.com/products/schd

## 경쟁
- toprank.txt('TIGER 미국배당다우존스' 블로그 상위 8, 11/21). 1(economicallyperson) 1천만~1억 월 분배금, 2(zebralife) 상품 소개, 4(7chanho7) 개인 10월 분배금, 6(korjap9633) SCHD vs TIGER 차이를 보수·세금·계좌로 글로만, 8(love820608) 다른 상품으로 옮긴 사례. 같은 날 1억을 넣은 두 계좌의 실제 결과를 센 글 0편 → bench.md

## 질문
1. SCHD 직접 사는 것과 TIGER 사는 것, 수익이 다른가 — https://blog.naver.com/korjap9633/224477771227 (제목 'SCHD vs TIGER 미국배당다우존스, 40대에게 유리한 ETF는?') → 답: 3년 5개월 TIGER 63.2%·SCHD 61.7%(원화, 세금 전), 해마다 이긴 쪽 바뀜
2. 1억 넣으면 매달 얼마 받나 — https://blog.naver.com/economicallyperson/224483607275 (제목 'TIGER 미국배당다우존스 배당금, "1억 투자"하면 매달 들어오는 돈은?') → 답: 최근 12번 439원 기준 세전 월 25만원쯤
3. 원화로 사면 환율 걱정이 없나 — https://blog.naver.com/korjap9633/224477771227 ('TIGER를 원화로 매수한다고 해서 환율 위험이 사라지는 것은 아니다') → 답: 환헤지 안 함, 2026년 SCHD 달러 27.3%가 원화 17.7%·TIGER 17.0%
4. 분배금은 매달 같나 — https://blog.naver.com/7chanho7/224469651930 (제목 '… 배당금 및 월배당 지급일 정리', 10월 35원) → 답: 40번 26~48원

## 왜
- 왜 거의 같나: 같은 지수(S3 etfBaseIndex)·둘 다 환헤지 없음 — 원문에 '수익이 같아야 한다'는 문장은 없어 '같은 지수를 따라가니 크게 갈리지 않았다'까지만
- 왜 해마다 이긴 쪽이 바뀌나: 원문에 이유 없음 — 환율 자료(야후 vs FRED)만 바꿔도 0.9%포인트 움직여 한 해 차이와 같은 크기라는 것까지만 씀
- 왜 SCHD 15% 뗌: 직접 산 사람은 미국에서 배당 15%가 떼임(S4). 안 뗀 값 64.8%도 기록

## 그래서
- 수익만 보고 고르면 차이가 거의 없음 → 고를 기준은 받는 달(매달 vs 분기)·한국 세금·계좌
- 원화 상품도 환율을 탐 — 달러가 내리면 같이 덜 오름(2026년)
- 매달 분배금이 26~48원으로 오르내려 월 생활비로 쓰면 달마다 다름

## 누구라면
- 매달 받는 돈이 필요한 은퇴자: TIGER가 매달(40번), SCHD는 분기(14번) — 총수익 차이는 1.5%포인트 안
- 연금계좌(연금저축·IRP)·ISA로 모으는 사람: 국내 상장만 담을 수 있다는 차이는 이 글 숫자에 없음(세금·계좌는 schdacct1007 글)
- 이미 SCHD를 달러로 가진 사람: 3년 5개월 결과 차이 149만원/1억

## 함정
- 기간 하나만 보고 '국내가 낫다/SCHD가 낫다' 단정 — 2024년엔 SCHD, 2025년엔 TIGER
- 야후 분배 기록이 한 번 빠져 있었음(2023년 9월 33원) — 운용사 연간 합으로 확인하고 채움
- 환율 출처·시각에 따라 SCHD 원화 값이 0.6~1.5%포인트 달라짐

## 한계
- 한국 세금(분배금·판 차익)·환전 수수료·매매 수수료 뺌 — 실제 손에 남는 돈은 다름
- 2023년 9월 분배 날짜는 운용사 연간 합에서 역산해 9월 26일로 놓음(9월 말 기준일 전 거래일) — 하루 차이 영향은 작음
- 환율은 야후 KRW=X 하루 값 하나 — TIGER 기준가에 쓰는 환율·시각과 다를 수 있음(FRED로 바꿔 0.6%포인트 확인)
- 상장 뒤 3년 5개월 한 기간 — 다른 기간·하락장 결과는 다를 수 있음
- SCHD 총보수는 11/19 확인값(이번에 다시 안 엶)

## 대조
| 글 값 | 원문 값 | 출처 |
|---|---|---|
| TIGER 상장 2023년 6월 20일 | listedDate 20230620 · firstTradeDate 2023-06-20 | S3 raw/naver_etfan_458730_1121.json · S1 |
| 3년 5개월 TIGER 63.6%·SCHD 61.3% | +63.6 · +61.3(15% 뗌) | S1·S6 calc_out_1124.txt, 대조 S3 3년 연평균 18.14 vs 계산 18.16 |
| 1억 → 1억 6,356만원·1억 6,133만원 | 16,356만 · 16,133만 | S1·S6 calc_out_1124.txt |
| TIGER 분배 40번·SCHD 배당 14번 | 40 · 14 | S1·S2(연간 합 같음) calc_out.txt |
| 2024년 25.6 vs 27.1 · 2025년 2.6 vs 1.7 · 2026년 17.3 vs 17.4 | 같음 | S1·S6 calc_out_1124.txt |
| FRED 시작 환율 1,280.21원 → SCHD 62.3%·차이 1.3%포인트 | 1280.21 · 계산 | S5 raw/fred_DEXKOUS_20261124.csv, S6 calc_out_1124.txt |
| 최근 1년 분배 439원 ÷ 14,540원 = 3.02% · 1억 월 25만원 | 439 · 3.02 · 25.2만 | S1·S6 calc_out_1124.txt, S3 dividendPerShareTtm 439·dividendYieldTtm 3.0 |
| SCHD 최근 4번 1.055달러 ÷ 33.94 = 3.11% | 1.0550 · 3.11 | S1·S6 calc_out_1124.txt |
| TIGER 월 26~48원 · SCHD 3·6·9·12월 | 26(2025-04)·48(2024-11) · 배당 달 | S1 raw events, S2 |
| 2026년 SCHD 달러 26.3%·환율 1,443.6→1,342.1원·원화 17.4%·TIGER 17.3% | 같음 | S1·S6 calc_out_1124.txt |
| 미국 배당 원천징수 15% | Korea, South dividends 15 | S4 https://www.irs.gov/pub/irs-lbi/tax-treaty-table-1.pdf |
| TIGER 환헤지 안 함·총보수 0.01% | '환헤지를 하지 않으므로' · totalFee 0.01 · FunETF 총보수 0.0100% | S3 · S8 (2차 2곳) |
| SCHD 총보수 0.06% | 0.06% | S7 · stockanalysis.com/etf/schd expenseRatio 0.06%(11/24) · 경쟁 6 korjap9633 |

# 올리기 전 확인
- 2026-11-21 14:3x firemap-write-b(조사·작성 날, 발행 날 11/22 16:10 회차가 야후 다시 받아 11/21 종가로 갱신 여부 확인)
- 다시 연 주소: https://query1.finance.yahoo.com/v8/finance/chart/458730.KS (SCHD·KRW=X 같은 꼴, 11/21 13:3x 받음) · https://investments.miraeasset.com/tigeretf/ko/product/search/detail/index.do?ksdFund=KR7458730008 (분배금 현황 11/21) · https://m.stock.naver.com/api/stock/458730/etfAnalysis (11/21) · https://www.irs.gov/pub/irs-lbi/tax-treaty-table-1.pdf (11/21) · https://fred.stlouisfed.org/series/DEXKOUS (apis.fred 11/21) · https://www.schwabassetmanagement.com/products/schd (de1pair1117 11/19 값)
- 기준일: TIGER 2026-11-20 종가 · SCHD 2026-11-19 미국 종가 · 운용사 분배 표 2026.11.19 기준 · 네이버 2026.11.19 기준
- 바뀐 것: 처음 조사 — 없음
- 새로 찾은 것: 상장 뒤 같은 날 1억 두 계좌 3년 5개월 63.2% vs 61.7% · 해마다 이긴 쪽 바뀜(한 해 2%포인트 안) · 야후 2023년 9월 분배 33원 빠짐(운용사 합으로 확인) · 경쟁 글 실제 결과 센 글 0편
- 2026-11-22 15:23 firemap-write(발행 날): 야후 458730.KS·SCHD·KRW=X 다시 받음(raw/*_chart_20261122.json, fetch1122.py) → calc1122.py 결과 calc_out_1122.txt가 calc_out.txt와 숫자 전부 같음(TIGER 최신 종가 11/20 금요일, 짝 SCHD 11/19 그대로) · 미래에셋 상세 Playwright 다시(fetch_tiger5.py, XHR까지) — 총보수 칸 여전히 빈 값 · FunETF 458730 총보수 0.0100% 확인(S8) — 다시 연 주소: https://www.funetf.co.kr/product/etf/view/KR7458730009 (raw/funetf_458730_1122.html 11/22 15:23 받음) · FRED는 이번에 시간 초과(환율 계산은 야후 KRW=X, FRED는 대조용 11/21 값)
- 기준일: TIGER 2026-11-20 종가 · SCHD 2026-11-19 미국 종가 (발행 날 다시 확인, 바뀜 없음)
- 바뀐 것: 숫자 바뀜 없음(63.2%·61.7%·1억 6,317만·1억 6,168만·439원·3.03%·3.08% 그대로) · 출처 줄에 FunETF(총보수) 더함
- 조사 뒤 공표: data/release_calendar.json — 가격은 매일, TIGER 11월 분배(11월 말 기준) 발행 뒤 · 발행 날 종가 다시 받아 숫자 갱신
- 2026-11-24 07:46 firemap-write-b(발행 날): 야후 458730.KS·SCHD·KRW=X 다시 받음(raw/*_chart_20261124.json, fetch1124.py) → calc1124.py 결과 calc_out_1124.txt
- 다시 연 주소: https://query1.finance.yahoo.com/v8/finance/chart/458730.KS (SCHD·KRW=X 같은 꼴, 11/24 07:43) · https://investments.miraeasset.com/tigeretf/ko/product/search/detail/index.do?ksdFund=KR7458730008 (200, 11/24) · https://m.stock.naver.com/api/stock/458730/etfAnalysis (439·3.03·totalFee 0.0100, 11/24) · https://www.funetf.co.kr/product/etf/view/KR7458730009 (총보수 0.0100%, 11/24) · https://www.irs.gov/pub/irs-lbi/tax-treaty-table-1.pdf (200, 11/24) · https://fred.stlouisfed.org/graph/fredgraph.csv?id=DEXKOUS (2023-06-20 1,280.21·11/20 1,342.41, 11/24) · https://www.schwabassetmanagement.com/products/schd (403 — 대신 https://stockanalysis.com/etf/schd/ expenseRatio 0.06%, 11/24)
- 기준일: TIGER 2026-11-23 종가 · SCHD 2026-11-20 미국 종가(바로 전 미국 거래일)
- 바뀐 것: 상장 뒤 63.2%·61.7% → 63.6%·61.3% · 1억 1억 6,317만·1억 6,168만 → 1억 6,356만·1억 6,133만(차이 150만→220만원쯤) · 2026년 17.0·17.7 → 17.3·17.4(SCHD 0.7%포인트 앞섬 → 거의 같음) · SCHD 달러 27.3→26.3%·환율 1,334.8→1,342.1원 · FRED 시작 환율로 바꾸면 62.6→62.3%·차이 0.6→1.3%포인트 · 분배율 TIGER 3.03→3.02%·SCHD 3.08→3.11% · 1억 연 303→302만원 · 그림 00·01 다시(mkimg.py) · 결론(해마다 이긴 쪽 바뀜·한 해 2%포인트 안) 그대로
- 새로 찾은 것: 11/23 하루에 상장 뒤 차이가 1.49→2.24%포인트로 벌어짐 — 환율(1,334.8→1,342.1원)과 SCHD 11/20 하락이 겹침, 이 정도는 며칠 새 오감
- 조사 뒤 공표: data/release_calendar.json — 가격은 매일, TIGER 11월 분배(11월 말 기준) 발행 뒤
