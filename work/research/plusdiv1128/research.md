# plusdiv1128 자료조사 (카페 11/29 12:40 배당 칸 TBD-배당) — PLUS 고배당주 vs KODEX 200 매달 100만원 10·5·3년 적립 (계산 사례형 form 2)

## 상태 (11/28 06:29 write)
- 11/27 15:2x write 회차: 원자료 받기·calc.py 첫 계산(11/26 종가) — 묶음 안 만들고 멈춤
- 11/28 06:2x write 회차: 야후·네이버 종가 다시(11/27 종가)·한화 11월 분배 103원 보탬·삼성 KODEX 200 원문·경쟁 5편·질문 4개·조각·그림·검사·이해 시험·editgate
- 발행 회차(11/29 12:1x write): 11/27 종가가 마지막 거래일이라 숫자 그대로일 것 — 한화·삼성 페이지만 다시 열어 '올리기 전 확인' 날짜 갱신

## 검증
- 수요: kwvol 11/28 06:3x — KODEX200 100,500 · PLUS고배당주 21,710 · 국내고배당ETF 630 · 자동완성 'plus 고배당주 배당금·배당률·배당락일'(raw/ac_plus_1128.json)
- 우리 실측: #461 kdiv1121(11/21, PLUS 분배금 증가율 다섯 ETF 비교) — 대상 같지만 8일 지남·각도 다름(분배금 늘어난 폭 → 적립 결과) · textrule 형식 2·배당현금흐름
- 겹침: 11/29 07:40 elsjeonse·22:40 gmnew(부동산), 10:10 TBD-지수(이 글이 KODEX 200을 쓰니 10:10은 미국 지수로 — slots note에 적음) · 11/28 22:40 k1split1128(코스피 폭락한 날 나눠 넣기) — 그 글은 '폭락한 날 나눠 넣기 횟수', 이 글은 '고배당 vs 지수 10년 적립' · 11/28 12:40 hidiv1128은 미국 고배당 3종
- 경쟁: toprank 'PLUS 고배당주' 상위 8 — 3위 wisefather1113이 'PLUS vs 코스피200 1년·3년·5년(목돈)·6개월 하락장' 비교(가장 가까움) · 적립식(매달) 10년 금액·6월 고점 뒤 줄어든 비율·분배금 현금 합을 센 글 0편

## 원문
- S1 한화자산운용 PLUS 고배당주 상품 페이지 — 보수(연) 0.23% · 기초지수 FnGuide 고배당주지수(유동시가총액 상위 200 종목 중 예상 배당수익률 상위 30종목) · 상장일 2012.08.29 · 분배 기준일 매월 마지막 영업일 · 분배금 지급현황 2026.11.30 기준 12.02 지급 103원(과세표준 92)·10.30 103·09.30 103·08.31 103·07.31 103·06.30 86, 11/28 06:2x 받음(raw/plus_006273_1128.txt): https://www.plusetf.co.kr/product/detail?n=006273
- S2 삼성자산운용 KODEX 200 — 총보수 0.150% · 기초지수 KOSPI 200(200종목 시가총액 가중, 한국거래소 산출) · 분배 기준일 1·4·7·10월 마지막 영업일 · 분배 10/30 136·7/31 183·4/30 446·1/30 80·2025/10/31 140 · 11/27 종가 76,705, 11/28 06:2x 받음(raw/kodex_prod_1128.json·kodex_divid_1128.json): https://m.samsungfund.com/api/v1/kodex/product/2ETF01.do · https://m.samsungfund.com/api/v1/kodex/divid-info.do?id=2ETF01
- S3 (2차①) 야후 파이낸스 chart API 161510.KS·069500.KS 일별 종가·분배 events(배당락일), ~2026-11-27 종가, 11/28 06:2x 받음(raw/*.KS.json): https://query1.finance.yahoo.com/v8/finance/chart/161510.KS · https://query1.finance.yahoo.com/v8/finance/chart/069500.KS
- S4 (2차②) 네이버페이 증권 일별 종가 — 11/24~11/27 PLUS 20,920·20,850·20,830·21,055 · KODEX 200 78,660·73,140·73,395·76,705 = S3 같음(raw/naver_price_*_1128.json): https://m.stock.naver.com/api/stock/161510/price · https://m.stock.naver.com/api/stock/069500/price
- S5 소득세법 제129조(배당소득 원천징수 14%) + 지방소득세(소득세의 10%) = 15.4%: https://www.law.go.kr/법령/소득세법/제129조
- S6 S1~S4로 직접 계산(calc.py → calc_out.txt, mkimg.py 같은 규칙 assert) — 야후에 아직 없는 PLUS 11월 분배 103원(배당락 11/27)은 S1로 보탬

## 우리만 (calc_out.txt, 11/27 종가, 매달 첫 거래일 100만원, 분배 15.4% 떼고 다시 삼)
- 10년(120번, 1억 2,000만원): KODEX 200 2억 9,005만 · PLUS 2억 5,013만
- 6/22(KODEX 200 2026년 종가 최고) 적립 평가액 KODEX 200 5억 5,243만 · PLUS 2억 8,409만 → 11/27까지 -47.5% · -12.0%
- 5년 1억 2,041만 vs 9,917만 · 3년 6,155만(1.71배) vs 4,692만(1.30배)
- 분배 현금으로 받기 10년: 받은 분배(세후) PLUS 3,426만 · KODEX 200 1,213만, 합 2억 2,884만 vs 2억 7,748만
- PLUS 최근 1년 분배 1,109원 ÷ 21,055원 = 5.27%

## 질문
- Q1 국내 고배당 ETF만으로 은퇴(생활비)가 되나(지식iN '국내 고배당주 ETF 투자만으로 은퇴 가능???'): https://kin.naver.com/qna/detail.naver?dirId=40102&docId=490544558 → 우리 답: 1억원어치면 최근 1년 분배율 5.27%로 1년 약 527만원·한 달 44만원쯤(세전), 10년 적립 때 받은 분배금 세후 3,426만원
- Q2 고배당 ETF를 계속 적립해도 되나(지식iN '고배당etf관련질문'): https://kin.naver.com/qna/detail.naver?dirId=40102&docId=491633850 → 우리 답: 매달 100만원 10년이면 PLUS 2억 5,013만, 같은 돈 KODEX 200 2억 9,005만(권유 없이 결과만)
- Q3 고배당 ETF 적립식이 맞는 방법인가(지식iN 'SCHD 같은 고배당ETF 적립식 투자가 맞나요?'): https://kin.naver.com/qna/detail.naver?dirId=40102&docId=466031005 → 우리 답: 10·5·3년 모두 지수(KODEX 200) 적립이 더 남았지만, 6월 고점 뒤 다섯 달은 고배당 쪽이 덜 줄었음(-12.0% vs -47.5%)
- Q4 PLUS 고배당주 배당금·배당률(네이버 자동완성 'plus 고배당주 배당금'·'plus 고배당주 배당률'): https://ac.search.naver.com/nx/ac?q=plus%20%EA%B3%A0%EB%B0%B0%EB%8B%B9%EC%A3%BC&st=100&r_format=json → 우리 답: 7월부터 매달 103원, 최근 1년 1,109원·5.27%, 11월 분 12월 2일 지급
- (원 기록 raw/kin_1128.txt)

## 왜
- 왜 10년 끝값이 KODEX 200 쪽이 많나: 값(주가) 차이 — 원문(S1·S2)에 두 상품 결과 차이 이유는 없음. 담는 방법이 다름(30곳 예상 배당수익률 vs 200곳 시가총액)만 적고 이유로 단정 안 함. 보수 차이(연 0.08%p)로는 설명 안 됨(계산)
- 왜 6월 뒤 KODEX 200 쪽이 더 줄었나: KODEX 200 종가 148,355 → 76,705(-48.3%) vs PLUS 2026년 고점(2/20) 29,620 → 21,055(-28.9%) — 값이 더 빠졌기 때문. 왜 값이 더 빠졌는지는 원문에 없음(경쟁 3은 '반도체 쏠림'이라 적었지만 1차 확인 안 함 → 안 씀)
- 왜 15.4%: 소득세법 129조 14% + 지방소득세 1.4%(S5)
- 왜 11월 분배를 보탰나: 11/30 기준 분배의 배당락이 11/27이라 11/27 종가엔 이미 빠져 있음(S1 기준일·S3 10/29 배당락 꼴과 같음)

## 그래서
- 고배당 ETF와 지수 ETF를 고를 때 볼 것: 같은 기간 분배 다시 산 끝값·하락장에서 줄어든 비율·분배금 받는 달·총보수 — 숫자만, 권유 없음
- 분배금을 생활비로 쓸 사람은 '받은 분배금'과 '남은 주식' 합을 따로 봄

## 누구라면
- 분배금을 다시 사는 사람: 10년 KODEX 200 2억 9,005만 vs PLUS 2억 5,013만
- 분배금을 생활비로 쓰는 사람: 10년 받은 분배(세후) PLUS 3,426만 vs KODEX 200 1,213만, 합은 2억 2,884만 vs 2억 7,748만
- 최근 3년에 시작한 사람: 3,600만원 → 6,155만 vs 4,692만

## 함정
- 분배금을 많이 주면 오래 모은 돈도 더 많을 거라 여기기 — 10년 받은 분배는 PLUS가 세 배 가까이 많지만 합은 KODEX 200이 많음
- 올해 하락장만 보고 고르기 — 6월 뒤 다섯 달은 PLUS가 덜 줄었지만 10·5·3년 끝값은 KODEX 200이 많음
- 11월 27일 값만 보고 분배금을 빼먹기 — 11월 분(103원)은 배당락이 지나 12/2에 들어옴

## 한계
- 매달 첫 거래일 종가에 소수 주까지 산 것으로 침(실제는 1주 단위·매매 수수료 뺌) · 분배는 배당락일 종가로 다시 삼(실제 지급일은 며칠 뒤)
- 세금은 분배금 전액에 15.4%(실제 과세표준은 분배금보다 적은 달이 있음 — 11월 분 103원 중 92원) → 실제 세금은 조금 적음 · 금융소득종합과세·ISA·연금계좌 뺌
- 2016-12~ 시작, 시작일 바꾸면 금액 달라짐 · 11/27 이후 값 바뀜
- 6월 22일은 KODEX 200 기준 고점(PLUS 2026년 고점은 2/20)

## 대조
| 글 값 | 원문 값 | 출처 |
|---|---|---|
| 10년 매달 100만원 KODEX 200 2억 9,005만 · PLUS 2억 5,013만, 4,000만원 가까이 차이 | 29,005만 · 25,013만 | S6 calc_out.txt '10년 … 재투자' · 종가 S3 https://query1.finance.yahoo.com/v8/finance/chart/161510.KS · S4 https://m.stock.naver.com/api/stock/161510/price |
| 120번·1억 2,000만원 | 2016-12 ~ 2026-11 | S6 calc_out.txt '넣은 돈 12,000만' |
| 15.4% | 14% + 1.4% | S5 https://www.law.go.kr/법령/소득세법/제129조 |
| 6월 22일 KODEX 200 5억 5,243만 · PLUS 2억 8,409만 | 55,243만 · 28,409만 | S6 calc_out.txt '2026-06-22' |
| KODEX 200 종가 14만 8,355원 → 7만 6,705원 | 148,355 · 76,705 | S2 https://m.samsungfund.com/api/v1/kodex/product/2ETF01.do (11/27 76,705) · S3 https://query1.finance.yahoo.com/v8/finance/chart/069500.KS · S4 https://m.stock.naver.com/api/stock/069500/price |
| 줄어든 비율 -47.5% · -12.0%, 다섯 번 500만원 더 | -47.5 · -12.0 | S6 calc_out.txt |
| 5년 1억 2,041만 · 9,917만 / 3년 6,155만 · 4,692만, 1.71배 · 1.30배 | 12,041·9,917·6,155·4,692 · 1.710·1.303 | S6 calc_out.txt |
| 받은 분배 PLUS 3,426만 · KODEX 200 1,213만 / 합 2억 2,884만 · 2억 7,748만 | 현금 3,426·1,213 · 끝값 22,884·27,748 | S6 calc_out.txt '현금' |
| 분배율 5.27%, 1억 1년 약 527만·한 달 44만쯤 | 1,109 ÷ 21,055 | S1 https://www.plusetf.co.kr/product/detail?n=006273 · S6 calc_out.txt |
| 30곳(200곳 중 예상 배당수익률 상위) · KODEX 200 200곳 시가총액 | 원문 문구 | S1 https://www.plusetf.co.kr/product/detail?n=006273 · S2 https://m.samsungfund.com/api/v1/kodex/product/2ETF01.do |
| 총보수 0.23% · 0.15%, 1억 1년 8만원 차이 | 0.23 · 0.150 | S1 https://www.plusetf.co.kr/product/detail?n=006273 · S2 https://m.samsungfund.com/api/v1/kodex/product/2ETF01.do |
| PLUS 매달 · KODEX 200 석 달에 한 번 | 매월 마지막 영업일 · 1·4·7·10월 마지막 영업일 | S1 https://www.plusetf.co.kr/product/detail?n=006273 · S2 https://m.samsungfund.com/api/v1/kodex/divid-info.do?id=2ETF01 |
| PLUS 7월부터 103원, 11월 분 103원 12월 2일 | 07.31 103 · 11.30 기준 12.02 지급 103 | S1 https://www.plusetf.co.kr/product/detail?n=006273 |

# 올리기 전 확인
- 확인일: 2026-11-28 06:29 (write) — 발행 11/29 12:40, 1일 안. 발행 회차가 11/29에 다시 열면 이 칸을 고침
- 기준일: 2026-11-27 한국거래소 종가(11/28·29 주말)
- 다시 연 주소: https://www.plusetf.co.kr/product/detail?n=006273 · https://m.samsungfund.com/api/v1/kodex/product/2ETF01.do · https://m.samsungfund.com/api/v1/kodex/divid-info.do?id=2ETF01 · https://query1.finance.yahoo.com/v8/finance/chart/161510.KS · https://query1.finance.yahoo.com/v8/finance/chart/069500.KS · https://m.stock.naver.com/api/stock/161510/price · https://m.stock.naver.com/api/stock/069500/price · https://www.law.go.kr/법령/소득세법/제129조
- 바뀐 것: 11/27 15:2x 계산(11/26 종가) → 11/27 종가로 다시: PLUS 10년 2억 4,644만 → 2억 5,013만, KODEX 200 2억 7,754만 → 2억 9,005만 · 분배율 5.20% → 5.27%(11월 분 103원 보탬, 창 하루 밀림)
- 새로 찾은 것: 한화 11월 분배 103원(11/30 기준·12/2 지급·과세표준 92원) — 야후엔 아직 없음 · 삼성 KODEX 200 총보수 0.150%·분배 1·4·7·10월 · 네이버 fchart(수정주가)는 PLUS 값이 실제 종가와 달라 안 씀
- 조사 뒤 공표: data/release_calendar.json 해당 없음(다음 분배 공지는 12월 말)

## 경쟁 (bench.md — toprank 'PLUS 고배당주' 블로그 상위 8, 본문 5편)
- 3 wisefather1113 'PLUS vs 코스피200 1년 +6.41 vs +42.44·5년 +132.30 vs +134.85·6개월 -18.20 vs -31.87'(목돈 한 번) · 2 hwakseye1 분배금 32%·10월 -9.3% · 1 hsjkce 코스피 대신 PLUS · 4 yunnai04 1억이면 월 49만 · 7 stock_nomad 매일 10만원 118회차 기록 — 매달 적립 10·5·3년 금액·6월 고점 뒤 줄어든 비율·분배 현금 합 0편
