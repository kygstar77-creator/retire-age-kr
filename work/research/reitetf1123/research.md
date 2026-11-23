# reitetf1123 자료조사 (카페 11/23 16:10 배당 칸, firemap-write-b 11/22 10:4x 회차) — 리츠 ETF 1억 1년 실제 결과, 직접 계산형

## 검증
- 수요: kwvol 11/22 — 리츠ETF 3,360 · 고배당ETF 3,840 · 월배당ETF 2,910 · 미국배당ETF 2,770 (JEPQ 28,540·JEPI 7,960·커버드콜ETF 9,520은 11/20 jepq1120·11/23 07:40 qqqi1123·11/22 divoone1122와 겹쳐 뺌 · 배당락은 #426·#454와 겹쳐 뺌)
- 경쟁에서 터진 증거: toprank '리츠ETF' 상위 8편 중 6편이 2주 안 글(11/22) · 6위 agrowingseason 'KODEX 한국부동산리츠인프라 월배당 60원인데 안전할까' 댓글 6 · 4위 jysherpa '1억원에 얼마 들어올까' 댓글 4
- 겹침: 우리 reitetf1013(TIGER 리츠부동산인프라 세금 떼면 원금)·reitdiv0926(미국 리츠 배당률) — 국내 리츠 ETF 넷을 같은 날 1억으로 맞대 1년·2년 실제 결과와 특별배당 뺀 분배율을 센 글 0편 · 11/23 07:40 qqqi1123(나스닥 커버드콜)과 종목·각도 다름
- 칸: 11/23 16:10 배당(slots.json TBD-배당, 관문 기한 11/23 10:10)

## 원문
- S1 야후 파이낸스 chart API 일별 종가·분배 events 429740.KS·329200.KS·476800.KS·182480.KS, 11/22 10:4x 받음(raw/*.json, fetch.py): https://query1.finance.yahoo.com/v8/finance/chart/329200.KS
- S2 미래에셋자산운용 TIGER ETF '분배금 현황' 연간 표(2026.11.19 기준) 329200·182480 줄, 11/22 받음(raw/tiger_dist_page_1122.txt, fetch_tiger3.py): https://investments.miraeasset.com/tigeretf/ko/distribution/annual/list.do
- S3 삼성자산운용 Kodex 월중 분배금 공지 8~11월 476800 줄, 11/22 받음(raw/kodex_notice_*.html): https://www.samsungfund.com/etf/lounge/notice-view.do?no=80913
- S4 (2차①) 아시아경제 2026-09-10 KODEX 한국부동산리츠인프라 특별배당 반영(삼성자산운용 발표): https://core.asiae.co.kr/article/2026091009351213312
- S5 (2차②) 아시아경제 2026-10-01 PLUS K리츠 특별배당 반영(한화자산운용 발표): https://core.asiae.co.kr/article/2026100108595682684
- S6 (2차③) 헤럴드경제 코람코더원리츠 하나증권빌딩 매각 특별배당 8,900원: https://biz.heraldcorp.com/article/10890694
- S7 S1~S3으로 직접 계산(calc.py → calc_out.txt) — 분배 합은 S2(TIGER 둘)·S3(KODEX)와 대조
- S8 Kodex 9월·8월 공지(60원·29원): https://www.samsungfund.com/etf/lounge/notice-view.do?no=79533 · https://www.samsungfund.com/etf/lounge/notice-view.do?no=78713

## 경쟁
- toprank.txt('리츠ETF' 블로그 상위 8, 11/22). 본문 5편 bench_raw(bench_fetch.py). 6(agrowingseason) 60원은 특별배당이라 설명하고 손실 가능을 가상 예시(-30,000원)로만, 5(skyplus10) PLUS K리츠 상품·특별배당 소개, 8(cashinsight) TIGER 리츠 상품 소개, 1(rajya) 차입·리파이낸싱 위험 글, 4(jysherpa) 미국 리츠 1억 배당금. 국내 리츠 ETF를 같은 날 1억으로 사서 1년 실제 결과를 센 글 0편 → bench.md

## 질문
1. 분배금 받으면 주가 빠져도 괜찮나 — https://blog.naver.com/agrowingseason/224469580025 ('월분배금을 받아도 손실이 날 수 있을까?') → 답: 1년 전 1억이면 국내 셋 다 8,579만~9,241만원
2. 1억 넣으면 매달 얼마 — https://blog.naver.com/jysherpa/224474861645 ('1억원을 투자하면 배당금이 얼마일까?') → 답: 지금 가격 1억 세후 월 KODEX 82만(보통 달 64만)·PLUS 74만(42만)·TIGER 75만
3. 월배당 60원 계속 주나 — https://blog.naver.com/agrowingseason/224469580025 ('월 60원이 계속 유지된다는 의미는 아닙니다') → 답: 9~12월 네 번 특별배당 반영, 보통 달 29원
4. 분배율 10% 믿어도 되나 — https://blog.naver.com/skyplus10/224470877610 (제목 '월배당 10%의 매력, 지금 투자해도 괜찮을까?') → 답: 특별배당 빼면 PLUS 6.0%·KODEX 9.1%, TIGER는 주가가 내려 9.0→10.6%

## 왜
- 왜 분배율이 10%대: KODEX·PLUS는 특별배당(S3·S4·S5), TIGER는 분배금 33원 그대로인데 주가가 내려서(분배율 = 분배금 ÷ 주가)
- 왜 국내 리츠 ETF 주가가 내렸나: 원문(S1~S6)에 이유 없음 — 안 씀
- 왜 미국MSCI리츠는 늘었나: 주가 +4.9%(S1) — 미국 리츠 시장 이유는 원문 없음, 안 씀

## 그래서
- 분배율만 보고 고르면 1년 결과와 다를 수 있음 — 국내 셋 다 분배금보다 주가가 더 빠짐
- KODEX·PLUS 지금 분배금은 12월까지 — 내년 생활비 계획은 보통 달 기준으로
- 기간에 따라 순서가 바뀜(1년 TIGER 미국 1위, 2년 TIGER 리츠 1위)

## 누구라면
- 매달 생활비가 필요한 은퇴자: 1억 세후 월 42만~75만원(보통 달 기준)인데 원금은 1년 새 8~14% 줄었음
- 9~10월 60원·131원 보고 산 사람: 12월 뒤엔 보통 달 금액으로 돌아갈 수 있음(운용사 발표가 4차례)
- 금융소득이 많은 사람: 분리과세 9.9% 신청 여부로 세후가 달라짐(S4·S5, 이번 계산은 15.4%)

## 함정
- 분배율은 주가가 내리면 올라가 보임 — TIGER 같은 33원이 9.0%→10.6%
- 최근 12번 분배율에 특별배당 섞임 — KODEX 11.6% vs 보통 달 9.1%, PLUS 10.5% vs 6.0%
- 1년 하나로 단정 — 2년으론 TIGER 리츠가 미국MSCI리츠보다 앞섬

## 한계
- 세금 15.4% 하나로 셈 — 분리과세 9.9%·연금계좌·ISA는 다름, 매매 수수료는 안 뺌(총보수는 가격에 들어 있음)
- 분배금 재투자 안 함 — 재투자하면 숫자 조금 다름
- PLUS K리츠 분배 기록은 야후 값(한화 공식 표는 이번에 안 엶, 131원은 S5 보도와 같음) · PLUS 3년은 야후 분배 34번(36달 중)이라 안 씀
- 미국MSCI리츠는 합성·환헤지 상품, 미국 시장 수익과 다를 수 있음
- 2025-11-20~2026-11-20 한 기간 — 다른 기간 결과는 다름

## 대조
| 글 값 | 원문 값 | 출처 |
|---|---|---|
| 1년 1억 → PLUS 8,218만·KODEX 8,581만·TIGER 리츠 9,060만·미국MSCI리츠 1억 521만 | 8,218 · 8,581 · 9,060 · 10,521 | S1·S7 calc_out.txt https://query1.finance.yahoo.com/v8/finance/chart/329200.KS |
| 분배금 700만·782만·759만·292만 | 같음 | S1·S7 calc_out.txt https://query1.finance.yahoo.com/v8/finance/chart/329200.KS |
| 주가 -24.8·-22.0·-17.0·+2.3% | 같음 | S1 https://query1.finance.yahoo.com/v8/finance/chart/329200.KS |
| 2년 1억 156만·1억 64만·9,429만·9,125만 | 같음 | S1·S7 calc_out.txt https://query1.finance.yahoo.com/v8/finance/chart/329200.KS |
| 3년 TIGER 리츠 +6.9%·미국MSCI리츠 +25.7% | 같음 | S1·S7 calc_out.txt https://query1.finance.yahoo.com/v8/finance/chart/329200.KS |
| 고점 대비 PLUS -48.8%·TIGER -44.4% | 10,225→5,240 · 6,590→3,665 | S1 https://query1.finance.yahoo.com/v8/finance/chart/329200.KS |
| TIGER 리츠 매달 33원 · 2026년 330원·2025년 379원 | 33 · 330 · 379 | S2 https://investments.miraeasset.com/tigeretf/ko/distribution/annual/list.do |
| 미국MSCI리츠 월 10~50원 · 2026년 369원 | 10(26.02)·50 · 369 | S2 https://investments.miraeasset.com/tigeretf/ko/distribution/annual/list.do |
| KODEX 8월 29원·9~11월 60원 | 29 · 60 · 60 · 60 | S3 https://www.samsungfund.com/etf/lounge/notice-view.do?no=80913 |
| PLUS 9월 131원·10월 122원 | 131(9/30 기준) | 2차 S5 https://core.asiae.co.kr/article/2026100108595682684 · S1 https://query1.finance.yahoo.com/v8/finance/chart/429740.KS |
| 특별배당 9~12월 네 번(KODEX·PLUS) | 9~12월 4차례 | 2차 S4 https://core.asiae.co.kr/article/2026091009351213312 · S5 https://core.asiae.co.kr/article/2026100108595682684 |
| 코람코더원리츠 하나증권빌딩 매각 1주 8,900원 | 8,900원 | 2차 S5 https://core.asiae.co.kr/article/2026100108595682684 · S6 https://biz.heraldcorp.com/article/10890694 |
| 분리과세 5천만원·3년·9.9% | 같음 | 2차 S4 https://core.asiae.co.kr/article/2026091009351213312 · S5 https://core.asiae.co.kr/article/2026100108595682684 |
| 분배율 KODEX 11.8%→9.3%·PLUS 11.0%→6.3%·TIGER 9.0→10.8% | 같음 | S1·S7 calc_out.txt https://query1.finance.yahoo.com/v8/finance/chart/476800.KS |
| 1억 세후 월 PLUS 78만(44만)·KODEX 84만(66만)·TIGER 76만 2천 | 77.6 · 44.1 · 83.5 · 65.6 · 76.2 | S1·S7 calc_out.txt https://query1.finance.yahoo.com/v8/finance/chart/476800.KS |

# 올리기 전 확인
- 2026-11-22 11:0x firemap-write-b(조사·작성 날, 발행 날 11/23 16:10 회차가 야후·분배 공지 다시 받아 11/21 이후 종가로 갱신 여부 확인)
- 다시 연 주소: https://query1.finance.yahoo.com/v8/finance/chart/329200.KS (429740·476800·182480 같은 꼴, 11/22 받음) · https://query1.finance.yahoo.com/v8/finance/chart/429740.KS · https://query1.finance.yahoo.com/v8/finance/chart/476800.KS · https://investments.miraeasset.com/tigeretf/ko/distribution/annual/list.do (11/22) · https://www.samsungfund.com/etf/lounge/notice-view.do?no=80913 (11/22) · https://core.asiae.co.kr/article/2026091009351213312 · https://core.asiae.co.kr/article/2026100108595682684 · https://biz.heraldcorp.com/article/10890694 (11/22)
- 기준일: 2026-11-20 종가 · 미래에셋 분배 표 2026.11.19 기준 · Kodex 11월 공지 2026.11.11
- 바뀐 것: 처음 조사(11/22) — 기준일 2026-11-20 종가 · 분배금 TIGER 리츠 33원(10월)·KODEX 60원(11월)·PLUS 122원(10월)·TIGER 미국MSCI리츠 41원(10월) · 발행 날(11/23) 회차가 야후·Kodex 공지 다시 받아 이 줄을 그날 숫자로 고친다(D-11 당일)
- 새로 찾은 것: 국내 리츠 ETF 셋 1년 1억 → 8,579만~9,241만원(분배금보다 주가 더 빠짐) · KODEX·PLUS 최근 분배에 특별배당(9~12월) · 특별배당 빼면 분배율 9.1%·6.0% · 경쟁 글 실제 결과 센 글 0편
- 조사 뒤 공표: data/release_calendar.json — 가격은 매일, 11월 말 분배(TIGER·PLUS 11/27 전후) 뒤 · 발행 날 종가 다시 받아 숫자 갱신
- 2026-11-23 15:53 firemap-write(발행 날 확인): 야후 chart 4종 다시 받음(장 마감 뒤 — 15:32 받은 값은 15:12 체결로 20분 늦어 버리고 15:53에 다시, 329200·476800·182480 regularMarketTime 15:30, 429740은 15:15 마지막 체결 5,240) · 분배 events 수 그대로(37·58·32·64, 새 분배 없음) · 기간을 2025-11-24→2026-11-23(2년 11/25, 3년 11/23 시작)으로 옮겨 calc.py 다시(calc_out_1120.txt가 옛 값)
- 기준일: 2026-11-23 종가
- 바뀐 것: 11/23 하루에 PLUS 5,470→5,240(-4.2%)·TIGER 리츠 3,745→3,665·KODEX 3,820→3,740·미국MSCI리츠 13,085→12,990 → 1년 1억 PLUS 8,579→8,218만·KODEX 8,757→8,581만·TIGER 9,241→9,060만·미국 1억 787→1억 521만 · 주가 하락 폭 15~21%→17~25% · 12번 분배율 KODEX 11.8·PLUS 11.0·TIGER 10.8% · 분배금 1주 값은 변경 0 · 글·그림 00·02·대조표 모두 이 값으로
- 새로 찾은 것: 발행 날 하루에 PLUS가 4% 넘게 빠져 1년 손실 폭이 3.6%p 커짐 — 기준일을 미리 박아 둔 글은 발행 날 종가로 다시 세야 한다
