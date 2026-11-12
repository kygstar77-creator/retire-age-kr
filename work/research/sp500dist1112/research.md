# sp500dist1112 자료조사 (카페 2026-11-12 18:40 칸 — firemap-write 11/12 09:2x) — 주식·ETF: 국내 상장 S&P500 ETF 분배금 차이

## 검증
- 수요: work/kwvol.py 11/12 — S&P500ETF 18,320 · 나스닥100ETF 6,350 · 월배당ETF 3,350 (월, PC+모바일). 축 근거: 순돌이 11/12 통계(배당ETF·지수 롱폼 중앙 460, 우리 주제 중 위)
- 겹침: 우리 카페 S&P500 ETF 글은 sp500etf(세금)·spvs0929(TIGER vs KODEX 수익)·tigersp(9월)·seqrisk1020 — 분배금 차이와 유보분 각도는 처음. 같은 축 최근 hdetf1109(고배당 분리과세, 11/9)·schdpair1105와 대상 다름
- 경쟁에서 터진 증거: toprank 'S&P500 ETF 분배금' 블로그 상위 8편 중 7편이 11/4~11/12 작성(지금 쓰이는 주제), 댓글 5·8·9·7(bench). 세 상품 분배금·수익률을 함께 놓은 글 0편, 2029년 뒤 KODEX 분배율 계산 0편

## 원문
- S1 삼성자산운용 KODEX 미국S&P500 분배금 현황 API — 2026-11-12 확인(raw/kodex_divid_2ETFE4.json): https://m.samsungfund.com/api/v1/kodex/divid-info.do?id=2ETFE4
- S2 삼성자산운용 공지 '삼성 KODEX 미국대표지수 ETF 분배금 지급 정책 안내'(2025.5.7, 본문 이미지 raw/notice66913_0.png) — 2026-11-12 확인: https://www.samsungfund.com/etf/lounge/notice-view.do?no=66913
- S3 미래에셋자산운용 TIGER 미국S&P500 상품 페이지 분배금 지급현황·수익률 — 2026-11-12 확인(raw/tiger_click.txt·raw/tiger_profit.html): https://investments.miraeasset.com/tigeretf/ko/product/search/detail/index.do?ksdFund=KR7360750004
- S4 한국투자신탁운용 ACE 미국S&P500 분배 이력·상품 정보 API — 2026-11-12 확인(../etfdist/ace_K55101D78195.json): https://papi.aceetf.co.kr/api/funds/K55101D78195/dividend?page=1 · https://papi.aceetf.co.kr/api/funds/K55101D78195
- S5 삼성자산운용 KODEX 미국S&P500 상품 API(1년 수익률 yieldYear1) — 2026-11-12 확인(raw/kodex_2ETFE4.json): https://m.samsungfund.com/api/v1/kodex/product/2ETFE4.do
- S6 소득세법 제129조 배당 원천징수 100분의 14 — 2026-11-12 확인(raw/law_sod129_1112.txt): https://www.law.go.kr/법령/소득세법/제129조
- S7 소득세법 제14조 이자·배당 2천만원 — 2026-11-12 확인(raw/law_sod14_1112.txt): https://www.law.go.kr/법령/소득세법/제14조
- S8 조세특례제한법 제91조의18 ISA 200만원·400만원·100분의 9 — 2026-11-12 확인(raw/law_jotuk91-18_1112.txt): https://www.law.go.kr/법령/조세특례제한법/제91조의18
- S9 (2차) 아시아경제 영문 2025-05-07 '유보 배당금 하반기부터 분배' — 2026-11-12 확인: https://www.asiae.co.kr/en/article/2025050709294866758
- S10 (2차) 머니투데이 2025-05-13 'KODEX 美 지수 ETF 유보 배당금 분배' — 2026-11-12 확인: https://www.mt.co.kr/stock/2025/05/13/2025051316163465664

## 경쟁
- bench.md 참조. 6위(press02)가 유보분과 2029년을 다뤘지만 KODEX 한 상품만, 2위(journeyfrom2025)는 TIGER 실제 입금액만. 세 상품 비교·1년 수익률 같음·1억원 세후·2029년 뒤 분배율·2천만원 기준 금액은 0편

## 질문
1. KODEX S&P500 분배금 왜 이렇게 많이 나오나 — https://blog.naver.com/press02/224470891174 (6위, 관련 글 제목 '분배금이 진짜 2배?', 댓글 9) → 답: c01(유보 배당 15분기 분배)
2. S&P500 ETF 분배금 1천만원 투자하면 얼마 — https://blog.naver.com/journeyfrom2025/224469168573 (2위 제목의 물음, 댓글 8) → 답: c03(1억원 기준 세후 금액, 상품별)
3. 분배금 많이 주는 ETF가 더 좋은가 — https://blog.naver.com/ggokyu/224469916595 (1위 '이렇게 많이 나오는지도 몰랐다는 친구', 댓글 5) → 답: c02(1년 수익률 거의 같음)

## 왜
- KODEX 분배금이 큰 이유: 2025년 1월 소득세법 시행령 개정으로 TR→분배형 전환, 상장~2024년 유보 배당을 15분기에 나눠 분기 NAV 약 0.27% 추가(S2)
- 수익률이 같은 이유: 분배금은 기준가격 안의 돈이 나오는 것 — 수익률은 분배금 재투자 가정(S3 '수익률 표는 투자분배금 재투자를 가정', S5 같은 안내). 운용사가 '같다'고 쓴 문장은 없음 → 숫자만 씀
- 시행령 개정 조문 자체(어느 조가 바뀌었나)는 원문에서 확인 못 함 → 글에 '소득세법 시행령이 바뀌면서'까지만

## 그래서
- 분배금 크기만 보고 고르면 2029년 1월 기준일 뒤 차이가 사라짐(S2·calc_out)
- 일반 계좌: 분배금이 클수록 15.4%를 먼저 냄(S6)
- 2천만원 기준: KODEX 약 9억 7천만원·ACE 약 21억원어치부터 종합과세 대상(S7·calc_out, 다른 이자·배당 0 가정)
- ISA: 200만원(서민형 400만원)까지 비과세, 넘으면 9.9%(S8)

## 누구라면
- 분배금을 생활비로 쓰려는 은퇴자: KODEX가 지금은 1억원당 월 약 14만 5천원으로 두 배지만 2029년 1월 기준일 뒤엔 비슷해짐
- 오래 모으기만 하는 일반 계좌 투자자: 분배금이 클수록 세금을 먼저 냄 → 다시 넣는 금액이 줄어듦
- ISA 투자자: 200만원까지는 분배금 크기와 세금 무관

## 함정
- '분배율 2%대'를 앞으로 받을 이율로 읽기 — 유보분이 끝나면 약 0.98%(S2·calc_out)
- 분배금이 많으면 수익도 많다고 읽기 — 1년 수익률 1.15~1.18%로 같음(S3·S4·S5)

## 우리만
- 운용사 세 곳 1차 자료로 2026년 분배금 합계·1년 수익률을 한 그림에 놓고, 1억원 세후 금액·유보분 뺀 KODEX 분배율·2천만원 걸리는 금액을 직접 계산(calc.py) — 경쟁 7편 0편

## 예외
- RISE·SOL 등 다른 S&P500 ETF는 넣지 않음(1차 자료 못 받음, FunETF만 — raw/funetf_*.txt). SOL은 월배당
- 환헤지(H)·커버드콜 S&P500 ETF는 다른 상품
- 연금저축·IRP는 세금 계산이 달라 다루지 않음
- 다른 이자·배당이 있으면 2천만원 기준 금액은 더 낮아짐

## 한계
- TIGER 1년 분배율은 분배금 합을 11/11 종가(25,020원)로 나눈 근사치 — 분배 당시 기준가격 아님
- 유보분 0.27%는 공지(2025.5.7 거래소 공시 기준) 값이라 분기마다 조금 다를 수 있음 → '약'으로 씀. 2029년 뒤 0.98%는 2026년 평균에서 0.27%를 뺀 추정
- 1년 수익률 분배금 재투자 가정 문구는 TIGER·KODEX만 확인, ACE는 확인 안 함
- 소득세법 시행령 개정 조문 확인 안 함

## 대조
| 글 값 | 원문 값 | 출처 |
|---|---|---|
| KODEX 2026년 분배금 486원 | 119·118·132·117원, annualTrend 2026 486 | S1 https://m.samsungfund.com/api/v1/kodex/divid-info.do?id=2ETFE4 |
| TIGER 253원 | 65·62·66·60원 | S3 https://investments.miraeasset.com/tigeretf/ko/product/search/detail/index.do?ksdFund=KR7360750004 |
| ACE 252원 | 65·62·66·59원 | S4 https://papi.aceetf.co.kr/api/funds/K55101D78195/dividend?page=1 |
| 2025년 4월부터 분기 분배, 시행령 개정 | 2025년 4월 분배 기준일부터 · 2025년 1월 소득세법 시행령 개정안 | S2 https://www.samsungfund.com/etf/lounge/notice-view.do?no=66913 |
| 상장~2024년 말 유보 배당 15번, 2025년 7월~2029년 1월 기준일 | 2021년 4월 9일~2024년 12월 · 총 15분기 · 2025년 7월~2029년 1월 | S2 |
| 분기마다 약 0.27% 더 | KODEX 미국S&P500 약 0.27% | S2 |
| KODEX 한 번 0.5% 안팎, TIGER·ACE 0.23~0.26% | 0.4916~0.5424% · ACE 0.2280~0.2604%, TIGER 60~66원/25,020원 | S1 · S4 · S3 |
| 1년 수익률 1.18·1.17·1.15% | yieldYear1 1.18 · yy1ErnRt 1.167 · 기준가격 1년 1.15 | S5 https://m.samsungfund.com/api/v1/kodex/product/2ETFE4.do · S4 https://papi.aceetf.co.kr/api/funds/K55101D78195 · S3 |
| 15.4% | 100분의 14 + 지방소득세 10% | S6 https://www.law.go.kr/법령/소득세법/제129조 |
| 1억원 세후 174만·86만·82만원 | 계산 1,744,706 · 855,468 · 818,759 | S1 · S3 · S4 · S6 · calc_out.txt |
| 유보분 빼면 KODEX 약 0.98% | 계산 0.982% | S1 · S2 · calc_out.txt |
| 2천만원 넘으면 합산 | 이자소득등의 종합과세기준금액 2천만원 | S7 https://www.law.go.kr/법령/소득세법/제14조 |
| KODEX 약 9억 7천만원·ACE 약 21억원 | 계산 9.70억 · 20.67억 | S1 · S4 · S7 · calc_out.txt |
| ISA 200만원(400만원), 넘으면 9.9% | 200만원 · 400만원 · 100분의 9(+지방 10%) | S8 https://www.law.go.kr/법령/조세특례제한법/제91조의18 |

# 올리기 전 확인
- 2026-11-12 09:4x(조사 날, firemap-write) S1·S3·S4·S5 받음, S2 공지 그림 확인 — **발행 회차(18:40)가 S1·S3·S4 분배 기록과 1년 수익률을 다시 받아 바뀐 것 적기**(다음 분배 기준일 2027년 1월 말이라 분배금은 안 바뀌고, 수익률만 바뀔 수 있음)
- 다시 연 주소: https://m.samsungfund.com/api/v1/kodex/divid-info.do?id=2ETFE4 · https://www.samsungfund.com/etf/lounge/notice-view.do?no=66913 · https://investments.miraeasset.com/tigeretf/ko/product/search/detail/index.do?ksdFund=KR7360750004 · https://papi.aceetf.co.kr/api/funds/K55101D78195/dividend?page=1 · https://papi.aceetf.co.kr/api/funds/K55101D78195 · https://m.samsungfund.com/api/v1/kodex/product/2ETFE4.do · https://www.law.go.kr/법령/소득세법/제129조 · https://www.law.go.kr/법령/소득세법/제14조 · https://www.law.go.kr/법령/조세특례제한법/제91조의18
- 기준일: 2026년 11월 12일(수익률·종가는 11월 11일)
- 바뀐 것: 조사 날이라 없음 — 10/30 기준일 분배금 세 상품 모두 11/3 지급 끝
- 새로 찾은 것: KODEX 유보 배당 15분기 분배(2029년 1월 기준일까지) · 세 상품 1년 수익률 1.15~1.18%
- 조사 뒤 공표: data/release_calendar.json에 운용사 분배 일정 없음(다음 분배 기준일 1월 마지막 영업일)
