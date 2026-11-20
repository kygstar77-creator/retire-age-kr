# kdiv1121 자료조사 (카페 11/21 10:10 배당 칸, firemap-write 11/20 09·12·15시 회차) — 국내 고배당 ETF 5개 월 분배금 1년 변화, 통계·기록형

## 검증
- 수요: kwvol 11/20 — PLUS고배당주 22,200 · 고배당ETF 3,910 · KODEX고배당주 3,330 · TIGER코리아배당다우존스 2,090
- 경쟁에서 터진 증거: toprank 'PLUS 고배당주 분배금' 1위 hwakseye1 '1년 새 32% 늘었는데…' 댓글 35(같은 날 다른 글 0~3)
- 겹침: 우리 SCHD 7편·jepq1120·mkifrec1120·kodex200_1120(지수)·divbear1121(미국 배당 ETF 하락장) — 국내 고배당주 ETF 분배금 추이는 0편
- 칸: 11/21 10:10 배당(slots.json, 관문 기한 11/21 04:10)

## 원문
- S1 한화자산운용 PLUS 고배당주 상품 페이지 분배금 지급현황(2025.03~2026.10 기준일·지급일·분배금·주당과세표준액)·기초지수·상장일, 11/20 09:3x 받음(raw/plus_006273.txt, fetch_plus4.py): https://www.plusetf.co.kr/product/detail?n=006273
- S2 한화자산운용 리포트 '[PLUS 고배당주] 월분배금 103원으로 상향…' 2026.07.29 — 분배 재원은 보유 종목 주식 배당금만, 103원은 예상 배당금으로 결정(raw/report_1910.txt): https://www.plusetf.co.kr/insight/report/detail?n=1910
- S3 (2차①) 야후 파이낸스 chart API 분배 events·일별 종가 161510·279530·104530·466940·0105E0(.KS), 11/20 받음(raw/y_*.KS.json, fetch_y.py): https://query1.finance.yahoo.com/v8/finance/chart/279530.KS
- S4 (2차②) 네이버페이 증권 ETF 분석 dividendPerShareTtm·dividendYieldTtm·보수·운용사 5개, 11/20 받음(raw/naver_etfan_*_1120.json): https://m.stock.naver.com/api/stock/279530/etfAnalysis
- S5 S3·S4 대조와 직접 계산(cmp_ttm.py → raw/cmp_ttm_1120.txt, calc.py → calc_out.txt) — 최근 12번 합이 5개 모두 S3=S4
- S6 삼성자산운용 KODEX 고배당주(2ETF96) 상품 페이지 — Cloudflare에 막혀 1차 못 받음(raw/kodex_2ETF96_1120.txt): https://www.samsungfund.com/etf/product/view.do?id=2ETF96

## 경쟁
- toprank.txt('PLUS 고배당주 분배금' 블로그 상위 8, 11/20). 1(hwakseye1) PLUS 하나 '1년 새 32%·한 달 -9.3%', 3(wisefather1113) PLUS vs KODEX 200 기간별 수익, 5(8509113) PLUS vs SOL 1,000만원당 월 분배금, 7(wisefather1113) 11월 103원 예정, 2(okor22) 종목코드 104530 오기. 같은 갈래 5개를 1년 새 월 분배금 증가로 줄 세운 글 0편 → bench.md

## 질문
1. PLUS 고배당주 분배금은 얼마나 늘었나 — https://blog.naver.com/wisefather1113/224457608317 (제목 '… 11월 배당금 103원 지급예정', '작년 11월(78원)보다 약 32% 많습니다') → 답: 78원 → 103원, 32%. 다섯 중 네 번째
2. PLUS 고배당주와 SOL 코리아고배당 중 매달 더 많이 받는 건 — https://blog.naver.com/8509113/224475578311 (제목 'PLUS 고배당주 팔고 SOL 코리아고배당으로 바꾼 이유… 1,000만 원당 월 분배금') → 답: 1억원·최근 달 기준 SOL 약 55만원, PLUS 약 48만원(세전)
3. 분배금이 늘었는데 주가는 왜 빠지나 — https://blog.naver.com/hwakseye1/224470204199 (제목 '… 주가는 왜 한 달 새 9% 빠졌을까?') → 답: 분배금과 주가는 따로 움직임, 1년 주가 KIWOOM은 내림
4. PLUS 고배당주 종목코드는 — https://blog.naver.com/okor22/224474473772 (제목 'PLUS 고배당주(104530)') → 답: 161510, 104530은 KIWOOM 코리아고배당

## 왜
- 왜 늘었나: PLUS는 운용사가 '보유 종목 배당금만 재원, 103원은 예상 배당금으로 결정'이라고 밝힘(S2). 나머지 4개는 원문에 이유 없음 → '찾지 못했어요'
- 왜 1년 전 같은 달과 비교: 월마다 금액이 바뀌어 비교하는 달에 따라 비율이 달라짐(KODEX 1월 45원) — 같은 달끼리
- 왜 1억 세전: 세율·과세표준이 상품·달마다 다름(PLUS 2월분 86원 중 과세표준 44원, S1) — 세금은 따로 안 셈

## 그래서
- 분배금 늘어난 비율만 보고 고르지 않기: 지금 받는 돈(1억 월 약 45만~55만원)·주가 1년 변화를 같이 봄
- 매달 공지되는 분배금은 운용사 페이지에서 확인(S1)
- 종목코드 확인하고 사기(161510 vs 104530)

## 누구라면
- 이미 PLUS 고배당주를 가진 사람: 다섯 중 증가율 4위·1억 월 4위권이라는 위치를 앎, 운용사가 밝힌 분배 원칙(S2)
- 월 생활비를 분배금으로 받으려는 은퇴자: 지금 금액(세전 1억당 월 약 45만~55만원)과 증가 추세가 다름
- 연금계좌로 사는 사람: 세금 때는 시점이 달라 위 세전 숫자 그대로 비교 가능(세율은 이 글에서 확인 안 함)

## 함정
- 이름 비슷한 ETF 코드 혼동(경쟁 2위 글이 PLUS를 104530으로 씀)
- 비교하는 달을 고르면 증가율이 커 보임(KODEX 1월 45원)
- 분배금 늘어도 주가는 내릴 수 있음(KIWOOM 1년 -1.4%)

## 한계
- KODEX·KIWOOM·TIGER·SOL은 운용사 1차 분배 내역을 못 받음(삼성 Cloudflare 막힘) — 야후+네이버 2차 2곳이 같은 값이라 씀
- 야후 분배 날짜는 배당락 쪽 날짜로 운용사 기준일과 하루쯤 다를 수 있음 — 달만 씀
- SOL은 2025년 11월 첫 분배라 1년 전 같은 달 없음
- 세금·수수료 뺌, 1억 월 분배금은 최근 달 금액이 이어진다고 친 값
- 분배금 증감 이유는 PLUS만 원문 있음

## 대조
| 글 값 | 원문 값 | 출처 |
|---|---|---|
| PLUS 78원 → 103원, 32% | 2025.10.30 기준 78 · 2026.10.30 기준 103 | S1 https://www.plusetf.co.kr/product/detail?n=006273 · S3 |
| KIWOOM 40원 → 80원, 두 배 | 2025-11-13 40 · 2026-11-12 80 | 2차 S3 https://query1.finance.yahoo.com/v8/finance/chart/104530.KS · S4 https://m.stock.naver.com/api/stock/104530/etfAnalysis (12번 합 895) |
| TIGER 72원 → 104원, 44% | 2025-10-30 72 · 2026-10-29 104 | 2차 S3 https://query1.finance.yahoo.com/v8/finance/chart/466940.KS · S4 https://m.stock.naver.com/api/stock/466940/etfAnalysis (합 1,060) |
| KODEX 53원 → 76원, 43% · 1월 45원 | 2025-10-30 53 · 2026-10-29 76 · 2026-01-29 45 | 2차 S3 https://query1.finance.yahoo.com/v8/finance/chart/279530.KS · S4 https://m.stock.naver.com/api/stock/279530/etfAnalysis (합 777) |
| SOL 60원, 첫 분배 2025년 11월 | 2025-11-13 95(첫) · 2026-11-12 60 | 2차 S3 https://query1.finance.yahoo.com/v8/finance/chart/0105E0.KS · S4 https://m.stock.naver.com/api/stock/0105E0/etfAnalysis (합 721) |
| KIWOOM 12월~5월 네 번 올림 | 40→60(12월)→70(2월)→75(4월)→80(5월) | 2차 S3 · S4 (위 주소) |
| PLUS 1월·7월 두 번 올림 | 78→86(2026.01.30)→103(2026.07.31) | S1 · S2 https://www.plusetf.co.kr/insight/report/detail?n=1910 |
| 보수 0.23·0.30·0.19·0.30·0.15% | 네이버 ETF 분석 totalFee | 2차 S4 https://m.stock.naver.com/api/stock/161510/etfAnalysis · S1(PLUS 0.23) |
| PLUS 2012년 상장, 예상 배당수익률 상위 30종목 | 2012.08.29 · '유동시가총액 상위 200 종목 중 … 상위 30종목' | S1 |
| PLUS 분배 재원은 보유 종목 배당금, 103원은 예상치로 결정 | '보유 종목에서 발생한 주식 배당금만을 분배 재원' | S2 |
| PLUS 2월분 86원 중 과세표준 44원 | 2026.02.27 기준 86 · 44 | S1 |
| 1억 월 세전 SOL 약 55만·KIWOOM 53만·KODEX 48만·PLUS 48만·TIGER 45만 | 545,160 · 525,200 · 484,956 · 476,375 · 446,056 | S5 calc_out.txt (S3 종가) |
| 1년 주가 KODEX +14.3·TIGER +12.4·SOL +5.2·PLUS +4.4·KIWOOM -1.4% | 같음 | S5 calc_out.txt (S3 종가) |

# 올리기 전 확인
- 2026-11-20 15:3x firemap-write(조사·작성 날, 발행 날 11/21 10:10 회차가 야후·네이버·PLUS 페이지 다시 받아 종가·분배금 갱신)
- 다시 연 주소(11/20): https://www.plusetf.co.kr/product/detail?n=006273 · https://www.plusetf.co.kr/insight/report/detail?n=1910 · https://query1.finance.yahoo.com/v8/finance/chart/161510.KS · https://query1.finance.yahoo.com/v8/finance/chart/279530.KS · https://query1.finance.yahoo.com/v8/finance/chart/104530.KS · https://query1.finance.yahoo.com/v8/finance/chart/466940.KS · https://query1.finance.yahoo.com/v8/finance/chart/0105E0.KS · https://m.stock.naver.com/api/stock/161510/etfAnalysis · https://m.stock.naver.com/api/stock/279530/etfAnalysis · https://m.stock.naver.com/api/stock/104530/etfAnalysis · https://m.stock.naver.com/api/stock/466940/etfAnalysis · https://m.stock.naver.com/api/stock/0105E0/etfAnalysis
- 기준일: 야후 2026-11-19 종가 · 분배금 2026-10~11월 지급분
- 바뀐 것: 처음 조사 — 없음
- 새로 찾은 것: 5개 월 분배 1년 증가율(KIWOOM 두 배·TIGER 44%·KODEX 43%·PLUS 32%) · KODEX 1월 45원으로 줄었다 다시 늘어남 · PLUS 2월분 과세표준 44원 · 경쟁 글 5개 줄 세운 글 0편
- 조사 뒤 공표: data/release_calendar.json — 분배금은 매달 말 공지, 발행 날 다시 받아 확인
