# kofinpair1124 자료조사 (카페 11/24 22:40 배당 칸 — 쇼츠 de1s_kofin m51UDa2pd-g 짝 글, firemap-write-b 11/23 13:40 회차) — 배당 ETF, 직접 계산형

## 검증
- 수요: 쇼츠 짝 글(사장님 10/11 '유튜브에 올린 것은 카페에도 반드시 글') · kwvol 고배당ETF 3,790·고배당주ETF 630(11/23) · 쇼츠 이해 시험 남은 궁금증 '금융 덜 든 고배당 ETF'(cardshorts/de1s_kofin/understand.md)
- 경쟁에서 터진 증거: toprank '고배당 ETF 비교' 상위 8편 중 2편이 오늘(11/23) 글, adam6899 댓글 4·the_hye_jin 댓글 4
- 겹침: 쇼츠는 PLUS·SOL 둘만 — 이번은 7개, RISE 반도체 쏠림·지수 규칙이 새 사실 · tigerdj1122(11/24 07:40, 미국배당다우존스 vs SCHD)·kdiv1121과 다름
- 칸: 11/24 22:40 배당(관문 기한 11/24 16:40)
- selfcheck [중복] '고배당' 3건: #461 PLUS 분배금 증가율·#465 하락장 낙폭·#445 분리과세 — 업종 비중은 다 안 다룸(각도 다름, hold 안 함)

## 원문
- S1 한화 PLUS 고배당주·신한 SOL 코리아고배당 구성종목 11/20자 금융 합 — cardshorts/de1s_kofin/prepub_1121.txt (https://www.plusetf.co.kr/product/detail?n=006273 · https://www.soletf.com/ko/fund/etf/211097?tabIndex=3)
- S2 삼성 KODEX 고배당주 구성종목 11/20자: https://m.samsungfund.com/api/v1/kodex/product-pdf/2ETF96.do?gijunYMD=20261120 (raw/kodex_279530_20261120.json, calc.py → calc_out.txt)
- S3 미래에셋 TIGER 코스피고배당 구성종목 11/20자: https://investments.miraeasset.com/tigeretf/ko/product/chart/prdct-item-list.ajax?ksdFund=KR7210780003&prfPrd=Week01&fixDate=20261120&listCnt=100 (raw/tiger_210780_20261120.json)
- S4 한국투자 ACE 고배당주 구성종목(PDF) 11/23자: https://papi.aceetf.co.kr/api/funds/K55101EQ7660/pdf?size=50 (raw/ace_0139P0_20261123.json) · 상품 화면 https://www.aceetf.co.kr/fund/K55101EQ7660
- S5 KB RISE 대형고배당10TR 구성종목 11/20자: https://kbam.co.kr/api/products/etfs/4494/holdings?base_dt=20261120 · 상품 화면 https://kbam.co.kr/products/4494 (지수 규칙)
- S6 KB RISE 고배당 구성종목 11/20자(상위 30): https://kbam.co.kr/api/products/etfs/4454/holdings?base_dt=20261120
- S7 S2~S6 직접 합산 calc2.py → calc2_out.txt
- S8 네이버 증권 ETF 분석 업종 비중(2차 대조): https://m.stock.naver.com/api/stock/315960/etfAnalysis (raw/etf_*.json)
- S9 쇼츠 https://youtu.be/m51UDa2pd-g · 롱폼 https://youtu.be/mkAxQPGaDqc

## 경쟁
- toprank.txt('고배당 ETF 비교' 블로그 상위 8, 11/23). 6(adam6899)은 PLUS 구성종목 상위 5개·'금융 업종 비중이 높다 … 고배당주 ETF는 대부분 비슷한 모습', 1(money_info_999)은 분배율 vs 총수익·RISE 대형고배당10TR '삼성전자·SK하이닉스 비중이 절반이 넘어서 … 같다'(추측), 4(everythinginsight)는 추천 TOP5·'은행·금융주 집중형' 분류, 3(joker1514)은 SCHD vs 국내 1,000만원, 7(the_hye_jin)은 은행고배당 TOP10. 고배당 ETF 7개 금융 비중을 운용사 원자료로 같은 기준으로 더한 글 0편, RISE 반도체 비중을 숫자로 확인한 글 0편 → bench.md

## 질문
1. 고배당 ETF는 다 금융주 위주인가 — https://blog.naver.com/adam6899/224473556520 ('고배당주 ETF는 대부분 비슷한 모습') → 답: 7개 중 3개만 절반 넘음, 넷은 3분의 1 안팎
2. 금융이 덜 든 고배당 ETF는 — https://youtu.be/m51UDa2pd-g (쇼츠 이해 시험 남은 궁금증, cardshorts/de1s_kofin/understand.md) → 답: ACE 37.4·TIGER 32.6·RISE 32.2·28.0, 단 RISE는 반도체 두 종목이 절반
3. RISE 대형고배당10TR은 정말 삼성전자·SK하이닉스가 절반인가 — https://blog.naver.com/money_info_999/224475934017 ('비중이 절반이 넘어서 … 같다') → 답: 11/20자 26.6+23.7 = 50.3%
4. 고배당 ETF끼리 무엇이 다른가 — https://blog.naver.com/everythinginsight/224476991795 ('은행·금융주 집중형' 분류) → 답: 따라가는 지수의 종목 고르는 규칙

## 왜
- 왜 RISE는 반도체가 절반인가: 지수 점수가 유통시가총액×현금배당총액(S5 화면) — 덩치가 곱해짐
- 왜 ACE는 증권사가 많은가: 원문은 배당락 회복률·배당수익률·배당성향·ROE를 본다고만 적음 — 증권사가 왜 뽑혔는지 이유는 원문에 없음
- 왜 TIGER는 금융 18종목인데 32.6%인가: 50종목에 한 종목 최대 3.67% — 고르게 나눠 담음(지수 비중 규칙 원문은 확인 안 함)
- 왜 SOL·PLUS·KODEX는 절반 넘나: 상위 종목이 은행·보험·금융지주(S1·S2) — 지수 규칙 원문은 이번에 안 읽음

## 그래서
- 고배당 ETF를 고를 때 분배율 다음 구성종목(PDF) 탭에서 업종을 봄
- 은행·금융지주 이미 가진 사람은 SOL·PLUS·KODEX에서 금융이 더 쌓임
- 삼성전자·SK하이닉스 가진 사람은 RISE 두 개에서 반도체가 더 쌓임

## 누구라면
- 은행주 직접 보유자: 금융 절반 넘는 셋을 더하면 쏠림
- 삼성전자·SK하이닉스 보유자: RISE 둘은 겹침
- 처음 고배당 ETF 사는 사람: 이름이 '고배당'이어도 담은 업종이 다름

## 함정
- '고배당 ETF = 금융주'로 묶어 보는 것 — 7개 중 넷은 3분의 1 안팎, RISE는 반도체가 절반
- RISE 고배당 화면 비중이 상위 30종목뿐이라 전체로 읽는 것
- 날짜가 다른 비중끼리 비교(네이버 11/19 기준 = 운용사 11/20자 파일)

## 한계
- KODEX 주주환원고배당주·HANARO K고배당·KIWOOM 코리아고배당은 운용사 원자료를 못 받아 뺌(삼성 화면이 브라우저 확인 화면으로 막힘, NH-Amundi·키움 화면 구성종목 API 못 찾음) — 네이버 값 56.64·43.51·26.90은 2차 1곳뿐
- ACE만 11/23자(날짜 바꿔 받기 안 됨)
- RISE 고배당은 상위 30종목(93.33%)만 — 나머지 6.67%에 금융이 있으면 최대 34.6%
- TIGER 금융 분류: 한국자산신탁(2.99, 부동산 신탁)을 금융에서 뺌 — 네이버 34.11과 차이
- 업종 분류는 파이어맵 기준(운용사·네이버 분류와 조금 다름), 지수 비중 규칙(상한 등)은 RISE·ACE 말고는 원문 안 읽음

## 대조
| 글 값 | 원문 값 | 출처 |
|---|---|---|
| SOL 56.5% · PLUS 55.6% | 56.463 · 55.645 | S1 https://www.soletf.com/ko/fund/etf/211097?tabIndex=3 · https://www.plusetf.co.kr/product/detail?n=006273 |
| KODEX 고배당주 52.5% | 52.49 | S2 https://m.samsungfund.com/api/v1/kodex/product-pdf/2ETF96.do?gijunYMD=20261120 |
| ACE 37.4% · 20종목 · 증권 셋 19.0% | 37.36 · 20 · 6.46+6.39+6.13 | S4 https://papi.aceetf.co.kr/api/funds/K55101EQ7660/pdf?size=50 |
| TIGER 32.6% · 50종목 · 금융 18종목 · 최대 3.7% | 32.56 · 50(+원화예금) · 18 · 3.67 | S3 https://investments.miraeasset.com/tigeretf/ko/product/chart/prdct-item-list.ajax?ksdFund=KR7210780003&prfPrd=Week01&fixDate=20261120&listCnt=100 |
| RISE 대형고배당10TR 32.2% · 삼성전자 26.6 · SK하이닉스 23.7 · 둘 50.3 · 열 종목 | 32.17 · 26.55 · 23.72 · 50.27 · 10(+원화예금) | S5 https://kbam.co.kr/api/products/etfs/4494/holdings?base_dt=20261120 |
| RISE 고배당 28.0% · 두 종목 46.7 · 80종목 중 상위 30 · 나머지 6.7 | 27.98 · 46.68 · total_count 80 · 100−93.33 | S6 https://kbam.co.kr/api/products/etfs/4454/holdings?base_dt=20261120 |
| 유통 시가총액×현금배당 총액 점수로 열 종목 | '[유통시가총액*현금배당총액] 점수 … 상위 10종목' | S5 https://kbam.co.kr/products/4494 |
| 이름 끝 TR = 배당금을 나눠 주지 않고 다시 투자 | '배당금 재투자로 총수익 추구' | S5 https://kbam.co.kr/products/4494 |
| ACE 배당락 뒤 회복 보는 지수 | '배당락 회복률을 핵심 기준' KRX-Akros 고배당주20 | S4 https://www.aceetf.co.kr/fund/K55101EQ7660 |
| 운용사 6곳 | 한화·신한·삼성·미래에셋·한국투자·KB | S1~S6 |

# 올리기 전 확인
- 2026-11-24 22:4x firemap-write-b(발행 날) — fetch_1124.py로 운용사 5곳(TIGER 11/23자·ACE 11/24자·RISE 2종 11/24자·KODEX 11/24자)·네이버 증권 ETF 분석 10종(기준일 2026.11.23) 다시 받아 calc_1124.py → calc_1124_out.txt. 쇼츠 m51UDa2pd-g 공개 확인(oembed 200)
- 다시 연 주소: https://investments.miraeasset.com/tigeretf/ko/product/chart/prdct-item-list.ajax?ksdFund=KR7210780003&prfPrd=Week01&fixDate=20261120&listCnt=100 · https://papi.aceetf.co.kr/api/funds/K55101EQ7660/pdf?size=50 · https://kbam.co.kr/api/products/etfs/4494/holdings?base_dt=20261120 · https://kbam.co.kr/api/products/etfs/4454/holdings?base_dt=20261120 · https://m.samsungfund.com/api/v1/kodex/product-pdf/2ETF96.do?gijunYMD=20261120 (firemap-write 11/23 09:3x 받음) · https://www.plusetf.co.kr/product/detail?n=006273 · https://www.soletf.com/ko/fund/etf/211097?tabIndex=3 (video-producer 11/21 받음) · https://kbam.co.kr/products/4494 · https://www.aceetf.co.kr/fund/K55101EQ7660 · https://m.stock.naver.com/api/stock/161510/etfAnalysis · https://m.stock.naver.com/api/stock/0105E0/etfAnalysis
- 기준일: 본문 숫자는 운용사 구성종목 2026-11-20자(ACE 2026-11-23자) 그대로 — 본문에 날짜를 적어 둠
- 바뀐 것: 11/24자로 다시 더하면 KODEX 52.5→52.8 · ACE 37.4→37.5(증권 셋 19.0→19.2) · TIGER 32.6→32.5(11/23자) · RISE 대형고배당10TR 32.2→32.6(반도체 둘 50.3→49.6) · RISE 고배당 28.0→28.6(반도체 46.7→45.7, 나머지 50종목 6.7→6.8) · PLUS·SOL 운용사 11/24 파일은 curl로 못 받음(PLUS API 400, SOL은 브라우저 화면) — 네이버 2차 11.20→11.23 PLUS 56.01→56.08·SOL 56.57→56.47. 차이 모두 0.7%p 안, 순위·'절반 넘는 건 셋'·'RISE 반도체 절반 안팎'·TIGER 맨 위 한일시멘트 3.7% 그대로 → 본문은 날짜 적힌 11/20자 숫자 유지(날짜 섞지 않음, 사진 다시 안 만듦)
- 새로 찾은 것: ACE 맨 위 종목이 SNT다이내믹스 6.9%로 바뀜(본문은 금융 셋만 말함, 영향 없음)
- 조사 뒤 공표: data/release_calendar.json — 구성종목은 매일 바뀜, 분배금 기준일 11월 말(이 글은 분배금 숫자 없음)
