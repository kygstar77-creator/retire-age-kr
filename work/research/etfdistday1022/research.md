# etfdistday1022 자료조사 (firemap-write-b 2026-10-22) — 카페 10/22 16:40 칸(TBD·비축 0) · 장르 주식(ETF·배당) · 형식2(계산 사례형)

## 검증
- 수요: 네이버 VIEW '월배당 ETF 분배금 기준일'·'분배락'·'월배당 ETF 분배금 언제 사야' 결과에 9~10월 글 다수(bench_raw/s_*.html), 배투모 주간 인기글에 10월 분배금 글 15편 이상(조회 950~8,230, bench_raw/wk_31050378.json)
- 경쟁: 분배락 뜻·기준일·매수 마감 설명 글은 많음(vera_na7·ecokinder·apex81·wolbae_com) — 실제 분배락 날 가격 기록을 센 글 0편
- 시기: 10월 말일 기준 분배 10/30, 매수 마감 10/28 — 일주일 앞
- 겹침: m1cafe1014(월배당 100만원 필요 금액)·m1stot1013(분배금 최고 커버드콜 총수익)·divdrop1020(고배당 ETF 급락일)과 각도 다름 — 분배락 날 하루 매매 기록은 처음

## 원문
- S1 미래에셋 TIGER 미국배당다우존스 집합투자규약 제32조 — 지급기준일 매월 마지막 영업일, 2026-10-22 확인: https://investments.miraeasset.com/tigeretf/upload/etf/20260528072833000787.pdf
- S2 미래에셋 상품 페이지·분배금 지급 현황 — 2026-09-30 기준 39원·과세표준 39원, 2026-10-22 확인: https://investments.miraeasset.com/tigeretf/ko/product/search/detail/index.do?ksdFund=KR7458730009
- S3 삼성 KODEX 미국배당다우존스 신탁계약서 제39조의2 — 매월 15일(비영업일이면 직전 영업일), 2026-10-22 확인: https://www.samsungfund.com/upload/agreement/2ETFN9-B.pdf · 분배 내역 10/15 37원: https://www.samsungfund.com/api/v1/kodex/divid-info.do?id=2ETFN9
- S4 한국거래소 안내서 — 결제 T+2, 2026-10-22 확인: https://global.krx.co.kr/contents/GLB/01/0109/0109000000/guide_to_trading_in_the_korean_stock_market.pdf · 삼성자산운용 공지(기준일 2영업일 전 매수): https://www.samsungfund.com/etf/lounge/notice-view.do?no=64114
- S5 소득세법 제129조 ①2나(배당소득 14%) + TIGER 투자설명서 15.4%(소득세 14%·지방소득세 1.4%), 2026-10-22 확인: https://www.law.go.kr/법령/소득세법/제129조 · https://investments.miraeasset.com/tigeretf/upload/etf/20260528072833005612.pdf
- S6 KRX 휴장일 2026 — 10월 휴장 10/5·10/9뿐, 2026-10-22 확인: http://open.krx.co.kr/contents/MKD/01/0110/01100305/MKD01100305.jsp
- S7 네이버 증권 모바일 일별 시세(수정 안 한 KRX 시가·종가) 4개 2024-07~2026-10-22, 2026-10-22 받음: https://m.stock.naver.com/api/stock/458730/price (raw/nvm_*.json) — 수정주가인 siseJson은 분배락 하락이 지워져 버림(교훈)
- S8 Yahoo Finance chart events 분배락일·분배금 4개 2년(2차 — S2·S3 공시와 9·10월분 대조 일치), 2026-10-22 받음: https://query1.finance.yahoo.com/v8/finance/chart/458730.KS?range=2y&events=div (raw/yh_*.json)

## 경쟁
- bench.md 참조. 경쟁은 '분배락 날 가격이 분배금만큼 빠진다'를 원리로만 설명, 매수 마감일 표(wolbae_com), 실제 기록으로 확인한 글 없음

## 질문
1. 분배락일에 사면 분배금을 못 받나요 — https://m.search.naver.com/search.naver?where=m_view&query=%EB%B6%84%EB%B0%B0%EB%9D%BD → 답: c01(분배락 날 사면 그달 못 받음)
2. 월배당 ETF 10월엔 언제까지 사야 받나요 — https://blog.naver.com/wolbae_com/224439488272 → 답: c01(10/28 수요일, 15일 기준 상품은 다름)
3. 분배금 받은 날 ETF 가격이 왜 빠졌나요 — https://blog.naver.com/vera_na7/224439147955 → 답: c02·c03(평균으로 분배금만큼, 96번 기록)
4. 국내상장 외국 ETF, 팔았다가 배당락 전에만 다시 사면 분배금을 똑같이 받나요 — https://kin.naver.com/qna/detail.naver?dirId=40102&docId=465385876 → 답: c01(기준일 2영업일 전까지 사면 받음)·c02·c03(대신 분배락 날 가격이 평균으로 분배금만큼 빠짐, 96번 중 50 대 46)

## 왜
- 분배락 날 가격이 빠지는 이유: 분배금이 ETF 자산에서 나가 기준가가 그만큼 줄어듦(S5 투자설명서 '분배락 과표기준가격')
- 매수 마감이 기준일 2영업일 전인 이유: 결제 T+2(S4)
- 아침 가격 하락이 분배금과 딱 맞지 않는 이유: 미국 자산 ETF라 전날 밤 미국 증시 움직임이 섞임 — 원문에 별도 이유 없음, 우리 해석으로 c04에 '섞여 있다'고만 씀

## 그래서
- 할 일: 분배금을 받고 싶으면 기준일 2영업일 전까지 매수, 상품마다 기준일을 운용사 공시로 확인
- 하루 매매로 분배금만 챙기는 건 기록상 반반, 평균 손해(세금·수수료)

## 누구라면
- 일반 계좌: 분배금에서 15.4% 바로 뗌(과세표준 한도)
- ISA·연금저축: 세금 바로 안 떼지만 가격 하락은 같음

## 함정
- 기준일이 말일인 상품과 15일인 상품이 같은 지수에도 섞여 있음(S1·S3)
- 수정주가 차트로 보면 분배락 하락이 안 보임(S7 교훈)

## 우리만
- ETF 4개 분배락 2년 96번, 앞날 종가 매수→분배락 날 시가 매도+세후 분배금: 이득 50·손해 46·평균 −3.5원/주, 상품별 평균 분배금 vs 아침 하락 — 경쟁 0편 (calc.py·calc_out.txt)

## 예외
- 과세표준이 분배금보다 작으면 세금이 줄어 결과가 조금 나아짐(S5)
- 종가에 팔면 결과가 달라짐(그날 시장 움직임)

## 한계
- 분배락일·분배금은 Yahoo(2차) — 9·10월분은 운용사 공시(S2·S3)와 대조, 나머지 달은 대조 안 함
- 매매 수수료·호가 차이 안 넣음
- 세금은 분배금 전액 15.4%로 계산(과세표준 한도 반영 안 함)
- 표본 96번, 4개 상품만

## 대조
| 항목 | 원문 값 | 글 값 | 출처 |
|---|---|---|---|
| TIGER 기준일 | 매월 마지막 영업일 | 매달 마지막 영업일 | S1 |
| KODEX 기준일 | 매월 15일(비영업일이면 직전) | 15일 무렵 | S3 |
| 결제 | T+2 | 이틀 거래일 뒤(T+2) | S4 |
| 10월 마지막 영업일 | 10/30(금), 10/28~30 휴장 없음 | 10월 30일 금요일 | S6 |
| 매수 마감 | 기준일 2영업일 전 | 10월 28일 수요일 | S4·S6 |
| KODEX 10월 분배락 | 10/14(기준 10/15) | 14일 | S3·S8 |
| 세율 | 15.4% | 15.4% | S5 |
| 9월분 분배금 | 39원 | 39원 | S2 |
| 10/22 종가 | 14,570원 | 14,570원 | S7 |
| 686주·26,754·4,120·22,634원 | 계산 | 같음 | S2·S5·S7 (calc) |
| 2만 9천원 | 686×42=28,812 | 2만 9천원 정도 | S7 (calc) |
| TIGER 평균 분배금·하락 | 36.5·41.7 | 37원·42원 | S7·S8 (calc.py) |
| KODEX | 31.0·21.7 | 31원·22원 | S7·S8 (calc.py) |
| +7%프리미엄 | 90.8·85.8 | 91원·86원 | S7·S8 (calc.py) |
| 나스닥100커버드콜 | 109.4·91.2 | 109원·91원 | S7·S8 (calc.py) |
| 커버드콜 안 빠진 날 | 0/24+2/24 | 48번 중 두 번 | S7·S8 (calc.py) |
| 96번 결과 | 이득 50·손해 46·평균 −3.5 | 같음 | S7·S8 (calc.py) |
| TIGER 분배금 범위 | 26~48원 | 26원에서 48원 | S8 |

# 올리기 전 확인
- 날짜: 2026-10-22 (발행 당일)
- 다시 연 주소(2026-10-22): https://investments.miraeasset.com/tigeretf/upload/etf/20260528072833000787.pdf · https://investments.miraeasset.com/tigeretf/ko/product/search/detail/index.do?ksdFund=KR7458730009 · https://www.samsungfund.com/upload/agreement/2ETFN9-B.pdf · https://www.samsungfund.com/api/v1/kodex/divid-info.do?id=2ETFN9 · https://global.krx.co.kr/contents/GLB/01/0109/0109000000/guide_to_trading_in_the_korean_stock_market.pdf · https://www.samsungfund.com/etf/lounge/notice-view.do?no=64114 · https://www.law.go.kr/법령/소득세법/제129조 · https://investments.miraeasset.com/tigeretf/upload/etf/20260528072833005612.pdf · http://open.krx.co.kr/contents/MKD/01/0110/01100305/MKD01100305.jsp · https://m.stock.naver.com/api/stock/458730/price · https://query1.finance.yahoo.com/v8/finance/chart/458730.KS?range=2y&events=div
- 대조 출처 다시 연 기록: S1·S2·S3·S4·S5·S6 2026-10-22 서브 조사관이 원문 다시 열어 문구 확인, S7 16:4x 다시 받음(10/22 종가 14,570원), S8 16:4x 다시 받음
- 기준일: 2026-10-22 종가
- 바뀐 것: 분배금 글 — 당일 확인. TIGER 9월분 39원(지급 10/2) 그대로, KODEX 10/15 기준 37원(10/19 지급) 새로 나옴, 10월 TIGER 기준일 10/30
- 새로 찾은 것: 네이버 siseJson은 수정주가라 분배락 하락이 지워짐 → 모바일 API 원 시세로 다시 계산
- 조사 뒤 공표: 없음(data/release_calendar.json 해당 없음)
