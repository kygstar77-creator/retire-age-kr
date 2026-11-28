# krndx1129 자료조사 (카페 11/29 10:10 지수 칸 TBD-지수) — 국내상장 나스닥100 환노출 vs 환헤지 vs QQQ, 2026년 들어 (통계·기록형 form 4)

## 상태 (11/28 09:3x write)
- 11/28 09:1x write 회차: 원자료(야후·네이버·ECOS·미래에셋)·계산·그림·조각·검사·bench·compare·표지(연하늘로 바꿈)·crosscheck(Gemini)·selfcheck 0·이해 3차 7명 — 제목 환노출형으로 좁힘, QQQ×환율 곱 문장·11/20 예시 뺌(독자 혼란, 원문에 까닭 없음)
- 발행 회차(11/29 09:1x write): 11/27 종가가 마지막 거래일(11/28·29 주말)이라 숫자 그대로일 것 — 미래에셋·ECOS 다시 열어 '올리기 전 확인' 날짜 갱신

## 검증
- 수요: kwvol 11/28 — TIGER미국나스닥100 28,120 · 자동완성 'tiger 미국나스닥100(H)'(raw/ac_tiger_ndx.json)
- 경쟁에서 터진 증거: 배당투자모임 주간 인기 '국내상장 미국ETF 오늘 왜 오르는건가요?' 조회 2,707(같은 주 중앙 1,400대 위) · '나스닥100은 하락했는데 왜.. 국내상장나스닥은?' 1,276 (bench_raw/weekly_31050378.json)
- 겹침: 11/28 sq1pair1128(QQQ·SCHD 섞기, 원화 표 있음 — 각도는 비율), #469 나스닥100 ETF 네 곳 같은 날 수익 비교(11/2x, 환헤지 아님), #484 QLD·TQQQ · 11/28 spxyield·k1split과 상품 다름

## 원문
- S1 미래에셋자산운용 TIGER 미국나스닥100(133690) 상품 페이지 — '환노출형으로서 원달러 환율변동율을 반영한 기초지수 수익률 추종을 운용목표로 함' · '환헤지를 하지 아니함' · 총보수 연 0.0068% · 11/27 종가 158,625, 11/28 받음(raw/tiger_KR7133690008.txt): https://investments.miraeasset.com/tigeretf/ko/product/search/detail/index.do?ksdFund=KR7133690008
- S2 미래에셋 TIGER 미국나스닥100(H)(448300) — '환헤지를 실시함' · 총보수 연 0.07% · 11/27 종가 20,705(raw/tiger_KR7448300004.txt): https://investments.miraeasset.com/tigeretf/ko/product/search/detail/index.do?ksdFund=KR7448300004
- S3 한국은행 경제통계시스템 731Y001 원/미국달러 매매기준율 일별(raw/fx_ecos.json): https://ecos.bok.or.kr/
- S4 (2차①) 야후 파이낸스 chart API 수정종가 QQQ·133690.KS·448300.KS: https://query1.finance.yahoo.com/v8/finance/chart/QQQ · https://query1.finance.yahoo.com/v8/finance/chart/133690.KS · https://query1.finance.yahoo.com/v8/finance/chart/448300.KS
- S5 (2차②) 네이버 증권 siseJson 수정주가 133690·448300(raw/naver_sise_*.txt) = S4 같음: https://api.finance.naver.com/siseJson.naver?symbol=133690&requestType=1&startTime=20251201&endTime=20261127&timeframe=day · https://api.finance.naver.com/siseJson.naver?symbol=448300&requestType=1&startTime=20251201&endTime=20261127&timeframe=day
- S6 S1~S5로 직접 계산(calc.py → calc_out.txt, calc2.py → calc2_out.txt, mkimg.py assert)

## 질문
- Q1 나스닥100은 하락했는데 국내상장 나스닥은 왜 다르냐(배당투자모임 주간 인기 '주린이라 질문이 많습니다.. 나스닥100은 하락했는데 왜.. 국내상장나스닥은?' 조회 1,276): https://cafe.naver.com/ca-fe/cafes/31050378/articles/68992 → 우리 답: 한국 장 시간에 거래돼 전날 미국 장과 하루씩 엇갈림, 447거래일 중 119일 방향 반대 · 몇 달로 보면 큰 몫은 환율
- Q2 국내상장 미국ETF 오늘 왜 오르나(같은 카페 조회 2,707): https://cafe.naver.com/ca-fe/cafes/31050378/articles/69302 → 우리 답: 같은 이유(거래 시간·환율), 11/20·11/23 예
- Q3 고점 대비 하락률이 국내상장 미국 ETF는 왜 더 크나(같은 카페 '고점대비하락률(국내상장 미국etf)' 999): https://cafe.naver.com/ca-fe/cafes/31050378/articles/68941 → 우리 답: 환노출형 고점은 환율 최고 무렵 7/1이라 −23.5%, QQQ·(H)는 10월 고점 −14.3%·−14.4%
- Q4 TIGER 미국나스닥100(H)와 차이(네이버 자동완성 'tiger 미국나스닥100(H)'): https://ac.search.naver.com/nx/ac?q=tiger%20%EB%AF%B8%EA%B5%AD%EB%82%98%EC%8A%A4%EB%8B%A5100&st=100&r_format=json → 우리 답: 2026년 들어 (H) +3.2% vs 환노출 −2.2%, 7/1까지는 환노출 +27.8% vs (H) +17.0%

## 왜
- 왜 환노출형이 마이너스: S1 운용목표가 '원달러 환율변동율을 반영' — 환율 1,433.9→1,342.7(−6.4%, S3)이 QQQ 달러 +6.3%를 지움
- 왜 (H)가 QQQ보다 덜 올랐나(+3.2% vs +6.3%): 원문(S2)에 이유 없음 → 글에 '따로 나와 있지 않다'고 씀(헤지 비용 추정 안 씀)
- 왜 하루씩 엇갈리나: 국내 ETF는 한국 장에서 거래(S1 시세가 한국 종가), 미국 종가는 한국 시각 새벽 — 데이터로 119/447일 확인. 장중 값이 무엇으로 정해지는지(선물 등)는 1차 원문 못 찾음 → 안 씀
- 왜 고점이 7/1: 환율 최고 7/2 1,554.4(S3) 무렵 — 값으로 확인, 인과 단정은 '환율이 가장 높던 때'까지만

## 그래서
- 국내상장 나스닥100을 고를 때 볼 것: 상품 이름의 (H)·운용사 '환헤지 사항' 칸 · 같은 기간 환율 변화 · 총보수(0.0068% vs 0.07%) — 권유 없음
- 계좌 숫자를 미국 지수와 견줄 때는 하루가 아니라 같은 기간 환율까지 같이 본다

## 누구라면
- 2026년 1월에 산 사람: 환노출 9,783만 vs (H) 1억 324만(1억 기준)
- 7월 1일까지만 들고 있던 사람: 환노출 +27.8% vs (H) +17.0% — 반대
- 하루하루 미국 지수와 맞춰 보는 사람: 447일 중 119일 방향이 반대

## 함정
- 미국 지수 등락률을 국내상장 환노출형 계좌에 그대로 대어 보기 — 2026년 QQQ +6.3%인데 환노출형 −2.2%
- 하루 등락만 보고 '추종을 못 한다'고 여기기 — 11/23 −1.1%는 11/20에 −4.4%가 먼저 반영된 뒤

## 한계
- 분배금 반영 수정종가 기준, 세금·수수료·매매 호가 차이 뺌 · 출발일(2025-12-30)을 바꾸면 숫자 달라짐 · QQQ는 미국 2025-12-31 종가 출발(한국 12/30과 하루 차이)
- 일별 맞춤은 '한국 거래일 d ↔ d 전 마지막 미국 거래일' 규칙, 그 사이 미국 거래 없으면 뺌(calc.py)
- (H)가 덜 오른 까닭·장중 값 결정 방식은 1차 원문 없음 → 안 씀
- 11/27 미국은 추수감사절 다음 날 단축장

## 대조
| 글 값 | 원문 값 | 출처 |
|---|---|---|
| 1억 → TIGER 9,783만원쯤 · (H) 1억 324만원 | 162,151.3→158,625(−2.2%) · 20,054.8→20,705(+3.2%) | S4 https://query1.finance.yahoo.com/v8/finance/chart/133690.KS · S5 https://api.finance.naver.com/siseJson.naver?symbol=133690&requestType=1&startTime=20251201&endTime=20261127&timeframe=day |
| QQQ 달러 +6.3% | 2025-12-31→2026-11-27 수정종가 | S4 https://query1.finance.yahoo.com/v8/finance/chart/QQQ · S6 calc2_out.txt (2차 — 나스닥 원문 대조는 못 함, 야후 한 곳 + 계산) |
| 환율 1,433.9원 → 1,342.7원, 6.4% 내림 | 731Y001 2025-12-30 1,433.9 · 2026-11-27 1,342.7 | S3 https://ecos.bok.or.kr/ |
| 환노출형 · 환헤지를 실시함 · 총보수 0.0068% · 0.07% | 원문 문구 | S1 https://investments.miraeasset.com/tigeretf/ko/product/search/detail/index.do?ksdFund=KR7133690008 · S2 https://investments.miraeasset.com/tigeretf/ko/product/search/detail/index.do?ksdFund=KR7448300004 |
| 고점 QQQ 10/6 −14.3% · (H) 10/7 −14.4% · TIGER 7/1 −23.5% | 수정종가 최고·11/27 | S4 https://query1.finance.yahoo.com/v8/finance/chart/448300.KS · S5 https://api.finance.naver.com/siseJson.naver?symbol=448300&requestType=1&startTime=20251201&endTime=20261127&timeframe=day |
| 7월 2일 1,554.4원 | 731Y001 2026-07-02 | S3 https://ecos.bok.or.kr/ |
| 447거래일 중 119일 반대 · 11/20 미국 QQQ −5.7% → 11/23 TIGER −1.1% · 11/20 이미 내림(−4.4%) | calc_out.txt | S6 calc.py · S4 https://query1.finance.yahoo.com/v8/finance/chart/133690.KS · S5 https://api.finance.naver.com/siseJson.naver?symbol=133690&requestType=1&startTime=20251201&endTime=20261127&timeframe=day |
| 7월 1일까지 TIGER +27.8% · (H) +17.0% | mkimg.py 출력 | S4 https://query1.finance.yahoo.com/v8/finance/chart/448300.KS · S5 https://api.finance.naver.com/siseJson.naver?symbol=448300&requestType=1&startTime=20251201&endTime=20261127&timeframe=day |

# 올리기 전 확인
- 확인일: 2026-11-28 09:3x (write) — 발행 11/29 10:10, 1일 안. 발행 회차가 11/29에 다시 열면 이 칸을 고침
- 다시 연 주소: https://investments.miraeasset.com/tigeretf/ko/product/search/detail/index.do?ksdFund=KR7133690008 · https://investments.miraeasset.com/tigeretf/ko/product/search/detail/index.do?ksdFund=KR7448300004 · https://ecos.bok.or.kr/ · https://query1.finance.yahoo.com/v8/finance/chart/QQQ · https://query1.finance.yahoo.com/v8/finance/chart/133690.KS · https://query1.finance.yahoo.com/v8/finance/chart/448300.KS · https://api.finance.naver.com/siseJson.naver?symbol=133690&requestType=1&startTime=20251201&endTime=20261127&timeframe=day · https://api.finance.naver.com/siseJson.naver?symbol=448300&requestType=1&startTime=20251201&endTime=20261127&timeframe=day
- 기준일: 2026-11-27 한국거래소·미국 종가, 환율 2026-11-27 매매기준율
- 바뀐 것: 처음 조사 — 11/28 09:2x 받은 값 그대로(이전 값 없음)
- 새로 찾은 것: 미래에셋 133690 '환헤지를 하지 아니함'·448300 '환헤지를 실시함' 문구 · ECOS 7/2 1,554.4 최고 · 배당투자모임 주간 인기 질문 3편
- 조사 뒤 공표: data/release_calendar.json 해당 없음

## 경쟁 (bench.md — toprank '나스닥100 환노출 환헤지' 블로그 상위 8)
- 1 healthy_life_365(11/28, 2,462자·사진 8) '원화 강세엔 (H)가 나을까?' · 2 bennie87(1,550원→1,330원, 연금저축 마이너스) · 6 whduddnd49 작동 방식 가정 · 8 tuttle0327 H 뜻 — 2026년 실제 1억 끝값 두 곳·고점 날짜 차이·하루 엇갈림 횟수를 센 글 0편(본문 확인은 짧은 줄 기준)
