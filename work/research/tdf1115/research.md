# tdf1115 자료조사 (카페 2026-11-15 18:40 칸 — firemap-write 11/15 07:1x) — 주식·ETF 축: TDF 빈티지별 주식 비중과 최근 석 달 하락폭, 같은 2050의 운용사 차이

## 검증
- 수요: work/kwvol.py 11/14 23:1x 잰 값 — TDF 4,750(PC 1,590·모바일 3,160) (slots.json 배정 note)
- 겹침: 우리 제목 전수 343개 중 TDF·타겟데이트 0편 · dfopt1112(디폴트옵션, 고용노동부 공시)와 자료·각도 다름(이 글은 상장 TDF ETF 상품 공시) · 같은 날 10:10 pentax1115(연금계좌 세금)과 겹치지 않게 세제는 안 씀
- 경쟁에서 터진 증거: toprank 'TDF' 블로그 상위 8편 중 7편이 11/5~11/15 작성(raw/toprank.txt) · 6위 '내 퇴직연금만 왜 마이너스? 믿고 맡긴 TDF'(11/9) — 지금 하락이 화제 · 8편 모두 개념·고르는 법, 실제 상품의 빈티지별 주식 비중과 최근 하락폭을 맞댄 글 0편

## 원문
- S1 FunETF 상품 정보(운용사 공시 모음, 2차) KODEX TDF2030·2040·2050·2060 — 2026-11-15 확인(raw/funetf_*.txt, funetf_out.txt): https://www.funetf.co.kr/product/etf/view/KR7433970001 · https://www.funetf.co.kr/product/etf/view/KR7433980000 · https://www.funetf.co.kr/product/etf/view/KR7434060000 · https://www.funetf.co.kr/product/etf/view/KR70082V0008 (자산비중 26.09.30, NAV 수익률 26.11.13, 실부담비율, '환노출형')
- S2 FunETF RISE TDF2030·2040·2050 — 2026-11-15 확인: https://www.funetf.co.kr/product/etf/view/KR7442550000 · https://www.funetf.co.kr/product/etf/view/KR7442560009 · https://www.funetf.co.kr/product/etf/view/KR7442570008
- S3 네이버페이 증권 ETF 지표(2차, S1 대조 — 총보수·3개월·1년 수익률·순자산) — 2026-11-15 확인(raw/naver_*.json): https://m.stock.naver.com/api/stock/434060/integration · https://m.stock.naver.com/api/stock/433970/integration · https://m.stock.naver.com/api/stock/442570/integration
- S4 야후 파이낸스 일별 종가·분배 이벤트(2차, 직접 계산 대조) — 2026-11-15 확인(raw/yahoo_*.json, calc_out.txt): https://query1.finance.yahoo.com/v8/finance/chart/434060.KS?range=2y&interval=1d&events=div
- S5 한국은행 ECOS 731Y001 원/미국달러 매매기준율(1차) — 2026-11-15 확인(apis.ecos): https://ecos.bok.or.kr/ (8/13 1,415 · 11/13 1,332.4)
- S6 야후 파이낸스 VT 일별 종가(2차) — 2026-11-15 확인(raw/yahoo_VT.json): https://query1.finance.yahoo.com/v8/finance/chart/VT · 대조 https://api.nasdaq.com/api/quote/VT/historical?assetclass=etf (나스닥 일별 종가 162.39→155.30, raw/nasdaq_vt.json)

## 경쟁
(bench.md 7편) 1·2·3·7위는 TDF 개념·숫자 뜻·글라이드패스, 4·5위는 2030·2040·2050 선택법·적격 TDF 100% 한도, 6위는 10월 197개 중 191개 마이너스 보도 인용, 8위는 TDF·ETF 중복 비중 계산. 빠뜨린 것: 실제 상품 하나하나의 지금 주식 비중, 빈티지별 최근 하락폭, 같은 빈티지 운용사 간 3년 차이와 실부담비율

## 질문
1. TDF 2030·2040·2050은 뭐가 다른가? — https://blog.naver.com/royal23-/224471637937 ('TDF 2030·2040·2050 차이는?') → 답: c01(주식 비중 48.7→77.4%, 석 달 -4.5→-9.0%)
2. 내 퇴직연금 TDF는 왜 마이너스인가? — https://blog.naver.com/durty0623/224467530583 ('내 퇴직연금만 왜 마이너스?') → 답: c03(해외 주가 -4.4%와 환율 -5.8%가 겹침, 환노출형)
3. 2050과 2060 중 어느 걸 고르나? — https://blog.naver.com/ccd1122/224466421909 ('2050·2060 빈티지 고르는 법') → 답: c02(KODEX는 지금 주식 비중 77.4%로 같음, 석 달 -9.03 vs -9.01%)
4. 같은 은퇴연도인데 운용사별 수익률·수수료 차이는? — https://blog.naver.com/royal23-/224471637937 ('같은 은퇴연도를 목표로 해도 운용사별 수익률과 수수료에는 차이') → 답: c04(3년 7.8%p, 실부담비율 0.14 vs 0.43%)

## 왜
- 빈티지 숫자가 클수록 하락이 큰 이유: 주식 비중이 클수록(S1 자산비중) 주가 하락을 더 받음 — 같은 운용사 4개에서 비중 순서와 하락 순서가 같음
- 석 달 하락 이유: 해외 주식 ETF를 담은 환노출형(S1)이라 해외 주가(VT 달러 -4.37%, S6)와 원·달러 환율 하락(-5.84%, S5)이 겹침 → 원화 기준 약 -9.95%
- KODEX 2050·2060 주식 비중이 같은 이유: 원문에 없음(한계) — 글에 '공시에 따로 나오지 않았다'
- 같은 2050 3년 차이: 비용 차이(실부담 0.4266-0.1352=0.29%p/년, 3년 약 0.87%p)로는 일부만 — 나머지 원인 원문에 없음(한계)

## 그래서
- 내 TDF의 주식 비중을 FunETF·운용사 상품 페이지 '자산비중 및 구성'에서 기준일과 함께 확인(S1)
- 같은 빈티지끼리도 주식 비중·실부담비율이 다르니 같이 놓고 확인(S1·S2)

## 누구라면
- 은퇴가 가까운 2030 보유자: 주식 48.7%(KODEX)·46.5%(RISE), 석 달 -4.5%·-3.9%
- 은퇴가 먼 2050·2060 보유자: 주식 73.7~79.2%, 석 달 -7.8~-9.0%
- 같은 2050을 고른 사람: 운용사에 따라 3년 49.06%~56.85%

## 함정
- 숫자가 10년 더 커도 주식이 더 늘지 않을 수 있음(KODEX 2050=2060 77.4%)
- 총보수만 보면 RISE 0.01% — 실제로 빠지는 실부담비율은 0.14%(S2)
- 환노출형은 환율이 내릴 때 해외 주가와 함께 손실이 겹침

## 우리만
- 같은 운용사 KODEX 4개 빈티지의 주식 비중(48.7·64.4·77.4·77.4%)과 석 달 NAV 수익률(-4.54·-6.4·-9.03·-9.01%)을 한 줄로 맞댐, RISE 3개로 같은 순서 재확인 · ECOS 환율과 VT로 원화 기준 하락 -9.95% 직접 계산 · 같은 2050 3년 차이 7.79%p 중 비용 몫 0.87%p 계산 — 경쟁 8편 0편

## 예외
- ETF 9개만 봄 — 퇴직연금 TDF의 대부분인 공모펀드형(삼성한국형TDF 등)은 이 셈에 없음
- 환헤지형 TDF는 환율 영향이 다름(이 글 9개는 모두 환노출형)
- 석 달은 8/13~11/13 한 구간 — 다른 구간이면 순서가 달라질 수 있음

## 한계
- KODEX 2050·2060 비중이 같은 이유, RISE·KODEX 3년 차이의 자산별 원인은 원문에 없음
- 주식 비중은 9/30 기준, 수익률은 11/13 — 그 사이 비중 변화는 확인 안 함
- TIGER 2045는 네이버 1년 -0.47% · 직접 계산 1.94% · FunETF NAV 0.13%로 어긋나 1년 수익은 글에 안 씀
- FunETF는 운용사 공시를 모은 2차 자료 — 운용사 원 페이지(samsungfund·riseetf)는 자바스크립트로 그려져 이번에 따로 안 열었음, 네이버(S3)·야후(S4) 직접 계산으로 대조

## 대조
| 글 값 | 원문 값 | 출처 |
|---|---|---|
| KODEX 2030 주식 48.7%, 석 달 -4.5% | 자산비중 26.09.30 주식 48.7% · NAV 3개월 -4.54% | S1 https://www.funetf.co.kr/product/etf/view/KR7433970001 · S3 https://m.stock.naver.com/api/stock/433970/integration (-4.55) |
| KODEX 2040 주식 64.4%, 석 달 -6.4% | 64.4% · -6.4% | S1 https://www.funetf.co.kr/product/etf/view/KR7433980000 · S4 calc_out.txt(-6.62) |
| KODEX 2050 주식 77.4%, 석 달 -9.0%(-9.03%) | 77.4% · -9.03% | S1 https://www.funetf.co.kr/product/etf/view/KR7434060000 · S3 https://m.stock.naver.com/api/stock/434060/integration (-9.0) |
| KODEX 2060 주식 77.4%, 석 달 -9.0%(-9.01%) | 77.4% · -9.01% · 상장 2025.07.22 | S1 https://www.funetf.co.kr/product/etf/view/KR70082V0008 · S4 calc_out.txt(-9.90 종가) |
| RISE 2030 석 달 -3.9%, 2050 -7.8% | NAV 3개월 -3.85% · -7.77% | S2 https://www.funetf.co.kr/product/etf/view/KR7442550000 · https://www.funetf.co.kr/product/etf/view/KR7442570008 · S3 https://m.stock.naver.com/api/stock/442570/integration (-7.76) |
| 3년 RISE 2050 56.85%, KODEX 2050 49.06%, 차이 7.8%p | NAV 3년 56.85 · 49.06 → 7.79%p | S2 https://www.funetf.co.kr/product/etf/view/KR7442570008 · S1 https://www.funetf.co.kr/product/etf/view/KR7434060000 |
| 1천만원이면 3년 뒤 약 78만원 차이 | 1,000만×7.79%=77.9만 | S1·S2 · calc 직접 |
| 실부담비율 RISE 0.14%, KODEX 0.43%, 3년 쌓아도 1%p 안 됨 | 0.1352% · 0.4266% → 0.29%p×3=0.87%p | S2 https://www.funetf.co.kr/product/etf/view/KR7442570008 · S1 https://www.funetf.co.kr/product/etf/view/KR7434060000 |
| RISE 2050 주식 73.7% | 73.7% | S2 https://www.funetf.co.kr/product/etf/view/KR7442570008 |
| 환노출형 | FunETF 분류 '주식+채권 환노출형' | S1 https://www.funetf.co.kr/product/etf/view/KR7434060000 · S2 https://www.funetf.co.kr/product/etf/view/KR7442570008 |
| 원·달러 1,415원 → 1,332.4원, 5.8% | 2026-08-13 1,415 · 11-13 1,332.4 → -5.84% | S5 https://ecos.bok.or.kr/ |
| VT 달러로 4.4% | 162.39 → 155.30달러 -4.37% | S6 https://query1.finance.yahoo.com/v8/finance/chart/VT · https://api.nasdaq.com/api/quote/VT/historical?assetclass=etf |
| 원화로 약 10% | (1-0.0437)×(1-0.0584)-1=-9.95% | S5 https://ecos.bok.or.kr/ · S6 https://query1.finance.yahoo.com/v8/finance/chart/VT |
| 국내 상장 TDF ETF 9개 | 네이버 ETF 목록 'TDF' 13개 중 순자산 100억원 넘는 9개(2065·KIWOOM 3개 제외) | S3 https://finance.naver.com/api/sise/etfItemList.nhn · raw/naver_etflist.json |

# 올리기 전 확인
- 2026-11-15 07:2x firemap-write(발행 같은 날 — 18:40 발행 회차가 FunETF 수익률 기준일 다시 볼 것)
- 다시 연 주소: https://www.funetf.co.kr/product/etf/view/KR7433970001 · https://www.funetf.co.kr/product/etf/view/KR7433980000 · https://www.funetf.co.kr/product/etf/view/KR7434060000 · https://www.funetf.co.kr/product/etf/view/KR70082V0008 · https://www.funetf.co.kr/product/etf/view/KR7442550000 · https://www.funetf.co.kr/product/etf/view/KR7442570008 · https://m.stock.naver.com/api/stock/434060/integration · https://m.stock.naver.com/api/stock/433970/integration · https://m.stock.naver.com/api/stock/442570/integration · https://ecos.bok.or.kr/ · https://query1.finance.yahoo.com/v8/finance/chart/VT · https://api.nasdaq.com/api/quote/VT/historical?assetclass=etf · https://finance.naver.com/api/sise/etfItemList.nhn (07:1x~07:2x 받음) · https://www.funetf.co.kr/product/etf/view/KR7442560009 · https://query1.finance.yahoo.com/v8/finance/chart/434060.KS?range=2y&interval=1d&events=div · https://api.nasdaq.com/api/quote/VT/historical?assetclass=etf
- 기준일: 수익률 2026-11-13(금) 장 마감 기준가·종가, 자산비중 2026-09-30, 환율 매매기준율 2026-11-13
- 바뀐 것: 없음(오늘 조사)
- 새로 찾은 것: KODEX 2050·2060 주식 비중 같음(77.4%) · 원화 기준 해외 주식 -9.95%
- 조사 뒤 공표: 11/14(금) 이후 국내 장 없음(토요일) — 발행 회차(18:40)도 11/13 기준가 그대로
