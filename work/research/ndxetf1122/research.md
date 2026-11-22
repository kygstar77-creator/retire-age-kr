# ndxetf1122 자료조사 (카페 11/22 18:40 지수 칸, firemap-write 11/21 21:10 회차) — 같은 지수 국내 ETF 4곳 같은 날 1억, 직접 계산형

## 검증
- 수요: kwvol 11/21 — 나스닥100 287,700 · KODEX미국나스닥100 30,700 · TIGER미국나스닥100 27,290 · ACE미국나스닥100 6,790 · 나스닥100ETF 5,890 (seed.md)
- 경쟁에서 터진 증거: toprank '나스닥100 ETF 비교' 상위 8편 중 5편이 1주 안 글(11/21) · 1위 cndtlr1221 4종 비교 댓글 4 · 5위 ekttms2 댓글 2
- 겹침: ndx1121(하락장 뒤)·ndxspx1118(vs S&P)·qqqkr0927(직투 vs 국내 세금)·x1cafe1022(환헤지)·SQ-1(11/28 롱폼) — 운용사 네 곳끼리 같은 날 1억 결과는 0편
- 칸: 11/22 18:40 지수(slots.json, 관문 기한 11/22 12:40)

## 원문
- S1 야후 파이낸스 chart API 일별 종가·분배 events 133690·379810·367380·368590.KS, ~2026-11-20, 11/21 받음(raw/*.json): https://query1.finance.yahoo.com/v8/finance/chart/379810.KS
- S2 미래에셋자산운용 TIGER ETF '분배금 현황' 연간 표(2026.11.19 기준) 133690 줄, 11/21 받음(raw/tiger_dist_page_1121.txt, fetch_tiger.py): https://investments.miraeasset.com/tigeretf/ko/product/search/detail/index.do?ksdFund=KR7133690008
- S3 (2차①) 네이버페이 증권 ETF 분석 4종 — 총보수·상장일·기간 수익률·분배 TTM·기초지수, 11/21 받음(raw/naver_etfan_*_1121.json): https://m.stock.naver.com/api/stock/379810/etfAnalysis
- S4 소득세법 제129조(배당소득 원천징수 100분의 14), 11/21 받음(raw/law_income_129.txt): https://www.law.go.kr/법령/소득세법/제129조
- S5 지방세법 제103조의13(소득세 원천징수액의 100분의 10), 11/21 받음(raw/law_local_103_13.txt): https://www.law.go.kr/법령/지방세법/제103조의13
- S6 삼성자산운용 공지 2025.06.20 TR ETF 분배 의무(소득세법 시행령 제26조의2), 11/21 받음(raw/samsung_notice_67815.html): https://www.samsungfund.com/etf/lounge/notice-view.do?no=67815
- S7 (2차②) 한경 매거진 2025-01-22 KODEX 미국나스닥100TR 분배형 전환: https://magazine.hankyung.com/business/article/202501223967b
- S8 S1로 직접 계산(calc.py → calc_out.txt, calc2.py → calc2_out.txt) — 분배 합 S2와 대조, 기간 수익률 S3과 대조

## 경쟁
- toprank.txt('나스닥100 ETF 비교' 블로그 상위 8, 11/21). 1(cndtlr1221) 총보수·실부담비용·순자산·선택 기준, 3(doorway2) 규모·TER·분배율·1개월~1년 수익률, 4(pata_tradingstory) KODEX vs TIGER 2021년 5월부터 누적·연도별(두 곳만), 5(ekttms2) 초보용 소개. 네 곳 모두를 같은 날 1억으로 맞대 결과·세후를 센 글 0편 → bench.md

## 질문
1. 같은 나스닥100인데 어느 운용사가 수익이 더 좋나 — https://blog.naver.com/cndtlr1221/224484911136 ('같은 지수인데 앱 수익률이 다르게 보이는 진짜 이유') → 답: 5년 7개월 1억 차이 189만원, 한 해 0.7%p 안
2. 수수료(총보수) 차이가 얼마나 되나 — https://blog.naver.com/doorway2/224483233707 ('표시 총보수와 TER을 비교하면 결과가 달라집니다') → 답: 0.0068 vs 0.0062%, 1억 1년 600원 차이, 가격에 이미 빠짐
3. KODEX와 TIGER 차이 — https://blog.naver.com/pata_tradingstory/224485913752 (제목 'KODEX 미국나스닥100·TIGER 미국나스닥100 비교') → 답: KODEX 2억 3,304만 vs TIGER 2억 3,115만, KODEX는 2025년 4월 전 분배 0
4. 분배금은 얼마나 나오나 — https://blog.naver.com/ekttms2/224483947171 ('한국 상장 나스닥100 ETF 비교 … 쉬운 정리') → 답: 1년 160~935원, 분배율 0.6~1.3%

## 왜
- 왜 거의 같나: 같은 지수(S3 etfBaseIndex NASDAQ 100, KODEX는 Total Return) — '같아야 한다'는 원문 문장은 없어 '거의 같이 움직였다'까지만
- 왜 KODEX가 조금 앞섰나: 원문에 이유 없음 — 2025년 4월 전 분배 0(S1·S7)이라는 사실만 씀, 원인으로 묶지 않음
- 왜 15.4%: 소득세 14%(S4) + 그 10% 지방소득세(S5)

## 그래서
- 결과 차이가 작아 운용사 고르는 기준은 1주 가격(적립 금액)·분배 달·세금 계좌
- 월 10만원 적립이면 TIGER는 한 달 돈으로 1주를 못 삼, 나머지 셋은 3~4주
- 분배금은 1년 0.6~1.3%라 생활비 목적이면 맞지 않음(숫자만 제시)

## 누구라면
- 적은 돈으로 매달 모으는 사람: 1주 2만원대 세 곳이 맞춰 사기 쉬움
- 큰돈을 한 번에 넣는 사람: 1주 가격 차이는 상관없고, 5년 7개월 결과 차이 1억당 189만원
- 분배금을 다시 넣는 사람: 세금 15.4% 떼면 차이 227만원(연금계좌·ISA는 이 계산 밖)

## 함정
- 증권사 앱 기간 수익률은 분배금 뺀 가격만 보여 KODEX처럼 분배가 큰 상품이 덜 오른 것처럼 보일 수 있음(경쟁 1 지적 — 우리는 다시 산 값으로 셈)
- 총보수만 보고 고르기 — 차이 1억당 1년 600원, KODEX·ACE·RISE는 보수가 같은데도 결과가 다름
- 시작일 하나 — 다른 날 시작하면 순서가 바뀔 수 있음(1년 대조에서도 KODEX·RISE·ACE·TIGER 순 같음)

## 한계
- 매매 수수료·팔 때 세금(과세표준 기준가 차익) 뺌 — 실제 손에 남는 돈은 다름
- KODEX·ACE·RISE 분배금은 운용사 페이지로 대조 못 함 — 야후 최근 4번 합이 네이버 TTM과 같음(2차 2곳)
- 실부담비용(기타 비용·매매중개수수료)은 경쟁 글마다 숫자가 달라(1: 0.1305~0.1580, 3: 0.0970~0.0991) 원문 확인 못 해 안 씀
- 시작일 2021-04-09 한 기간

## 대조
| 글 값 | 원문 값 | 출처 |
|---|---|---|
| 2021년 4월 9일 KODEX 상장일·네 곳 중 가장 늦음 | listedDate 20210409 · 20101018·20201029·20201106 | S3 raw/naver_etfan_*_1121.json |
| 1억 → 2억 3,304만·3,209만·3,135만·3,115만 · 차이 189만원 | 2.3304·2.3209·2.3135·2.3115억 | S1·S8 calc_out.txt, 대조 S3 1년·5년 수익률 |
| 5년 7개월 | 2021-04-09~2026-11-20 | S1 |
| 해마다 27.4~27.5 · -30.6~-30.5 · 61.3~61.8 · 45.0~45.7 · 16.5 · -4.3~-4.1 | 같음 | S1·S8 calc2_out.txt |
| 15.4% 떼면 2억 3,239만·3,012만 · 227만원 | 2.3239·2.3012 | S1·S8 calc2_out.txt, S4·S5 |
| 배당소득 14% + 그 10% 지방소득세 = 15.4% | 100분의 14 · 100분의 10 | S4 https://www.law.go.kr/법령/소득세법/제129조 · S5 https://www.law.go.kr/법령/지방세법/제103조의13 |
| TIGER 1주 15만 5,220원 · 나머지 2만 3천~2만 7천원 | 155220 · 23180·26680·25875 | S1 raw/*.json 2026-11-20 |
| 1년 분배 935·290·160·181원 · 0.6~1.3% | dividendPerShareTtm 935·290·160·181 | S1 events · S3 · S2(TIGER 2026년 935) |
| KODEX 2025년 4월 전 분배 0, 그 뒤 석 달마다 | 첫 event 2025-04-29 · 7번 | S1 raw/379810.json · 2차 S3 기초지수 Total Return · S7 |
| 분배 달 1·4·7·10 / 3·6·9·12월 말 무렵 · 현금으로 두면 2억 2,933만~3,322만 | dividendMonthThisYear · events 날짜 | S1 · S3 |
| 총보수 0.0068% · 0.0062% | totalFee 0.0068 · 0.0062 | 2차 S3 https://m.stock.naver.com/api/stock/379810/etfAnalysis · 2차 https://blog.naver.com/cndtlr1221/224484911136 '연 0.0062퍼센트, TIGER가 연 0.0068퍼센트' |
| TIGER 2010년 상장 | listedDate 20101018 | S3 · S1(2016-11부터 기록) |

# 올리기 전 확인
- 2026-11-21 21:3x firemap-write(조사·작성 날, 주말이라 11/20 종가가 최신 — 발행 날 11/22 18:40 회차가 야후 다시 받아 같은지 확인)
- 다시 연 주소: https://query1.finance.yahoo.com/v8/finance/chart/379810.KS (네 종목 같은 꼴, 11/21) · https://investments.miraeasset.com/tigeretf/ko/product/search/detail/index.do?ksdFund=KR7133690008 (11/21) · https://m.stock.naver.com/api/stock/379810/etfAnalysis (4종 11/21) · https://www.law.go.kr/법령/소득세법/제129조 (11/21) · https://www.law.go.kr/법령/지방세법/제103조의13 (11/21) · https://www.samsungfund.com/etf/lounge/notice-view.do?no=67815 (11/21) · https://magazine.hankyung.com/business/article/202501223967b (seed 11/21) · https://blog.naver.com/cndtlr1221/224484911136 (경쟁 1, 11/21 본문 받음)
- 기준일: 2026-11-20 종가 · 운용사 분배 표 2026.11.19 기준 · 네이버 2026.11.19 기준
- 2026-11-22 18:21 firemap-write(발행 회차): 야후 4종(133690·379810·367380·368590) 다시 받음 — 마지막 종가 11/20 그대로(155,220·23,180·26,680·25,875원), 새 분배 없음
- 바뀐 것: 처음 조사 — 없음 · 11/22 다시 받아도 같음
- 새로 찾은 것: 네 곳 같은 날 1억 5년 7개월 189만원 차이·한 해 0.7%p 안 · 세후 227만원 · KODEX 2025년 4월 전 분배 0 · 경쟁 글 네 곳 결과 센 글 0편
- 조사 뒤 공표: data/release_calendar.json — 가격은 거래일마다(다음 11/23 월), 분배 다음 기준일 2027-01 말(RISE 12월 말) — 발행 날 11/22(일)은 새 종가 없음
