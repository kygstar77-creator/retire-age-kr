# de1pair1117 자료조사 (카페 2026-11-17 22:40 칸 — firemap-write 11/17 07:1x, 운영실장 대리) — 배당ETF: 쇼츠 de1s_basket 짝 글 'SCHD와 국내 미국배당다우존스 같이 사면 분산?'

## 검증
- 수요: work/kwvol.py 11/17 07:1x — SCHD 50,400 · TIGER미국배당다우존스 24,330 · 미국배당다우존스 4,420 · SCHD중복 10(말 자체는 안 쓰임 → 본문은 '나눠 담은 걸까'·'분산')
- 경쟁에서 터진 증거: toprank 'SCHD 미국배당다우존스 차이' 상위 8편 중 6편이 11/11~11/17 작성(toprank.txt) — 지금 화제 · 7편이 세금·계좌·분배 주기, '같이 사면 분산?'을 숫자로 따진 글 0편(3위 한 줄뿐)
- 짝 영상: 쇼츠 yX3f9ESewcg(11/17 19:20 공개 예정, cardshorts/de1s_basket/upload.json) — 질문 '둘 다 담으면 나눠 담은 걸까' 하나. n3pair1116(연봉 실수령액)·gmpair1116(광명 시세)과 다른 질문

## 원문
- S1 찰스 슈왑 SCHD 상품 페이지·보유 종목 파일(Export All Holdings, As-Of 2026-11-13, 102줄·Sector 칸) 2026-11-17 받음 https://www.schwabassetmanagement.com/products/schd → raw/schwab_SCHD_holdings_20261117.csv · raw/SCHD_page_20261117.txt('Total Expense Ratio 0.060%')
- S2 네이버 증권 ETF 분석 TIGER 미국배당다우존스(458730) 2026-11-17 받음(기준 2026.11.13) https://m.stock.naver.com/api/stock/458730/etfAnalysis → raw/etf_458730_20261117.json — sectorPortfolioList·etfTop10MajorConstituentAssets·navPerformanceList·totalFee·dividend·etfSummary('환헤지를 하지 않으므로 기초지수의 원화환산 수익률에 연동')
- S3 같은 API SOL(446720)·ACE(402970)·KODEX(489250) 2026-11-17 받음 https://m.stock.naver.com/api/stock/446720/etfAnalysis · https://m.stock.naver.com/api/stock/402970/etfAnalysis · https://m.stock.naver.com/api/stock/489250/etfAnalysis → raw/etf_*_20261117.json (ACE etfSummary '10년 연속 배당금을 지급한 미국상장 종목 중 우량 펀더멘털 … 상위 100종')
- S4 야후 파이낸스 SCHD 분배 기록 1년 2026-11-17 받음 https://query1.finance.yahoo.com/v8/finance/chart/SCHD?range=1y&interval=1mo&events=div → raw/yahoo_SCHD_div_20261117.json (2025-12·2026-03·06·09 네 번)
- S5 파이어맵 카페 #245 'SCHD 배당금 ISA나 연금저축에서 받으면 미국 세금 얼마나 빠질까'(schdacct1007, 계좌·세금) https://cafe.naver.com/firemap/245

## 경쟁
(bench.md 5편) 1위는 분배 주기·세금·계좌 차이 표, 3위는 '함께 산다고 크게 분산되는 것은 아니다' 한 줄(숫자 없음), 4위는 달러·원화 수익률 차이. 빠뜨린 것: 업종 비중을 SCHD·국내 4종 같은 날로 맞댄 숫자, 국내 4종이 많이 담은 종목이 SCHD에도 다 있다는 것, 국내 4종끼리 1년 수익률 차이

## 질문
1. 타이거미국배당다우존스가 schd 한국판인가여? — https://kin.naver.com/qna/detail.naver?dirId=40102&docId=482156098 → 답: c01(같은 지수·같은 종목)·c02(업종 차이 0.3%p 안)
2. 국내상장 미국배당 ETF 추천(토스에 SCHD 보유, ISA에 국내 상장 하나 더) — https://kin.naver.com/qna/detail.naver?dirId=40102&docId=493875868 → 답: c03(SCHD 옆에 국내 미국배당다우존스를 더해도 업종·종목·환율로 안 나뉨) · 추천은 안 함
3. 배당주 포트폴리오는 어떻게 구상해야되나요? — https://kin.naver.com/qna/detail.naver?dirId=40102&docId=494740968 → 답: c04(가진 ETF 업종 구성 보는 곳) · 무엇을 담으라는 권유는 안 함

## 왜
- 업종이 같은 이유: 다섯 상품 모두 Dow Jones U.S. Dividend 100 지수를 따라감(S2·S3 etfBaseIndex, SCHD는 S1 상품 페이지) — 글에 그대로
- 필수소비재·헬스케어·에너지에 몰린 이유: 원문(S&P 지수 방법론)은 안 읽음 → 글에 쓰지 않음(한계)
- 환율이 같이 움직이는 이유: TIGER '환헤지를 하지 않으므로 원화환산 수익률에 연동'(S2), SCHD는 달러 상품 — 글에 그대로

## 그래서
- 가진 ETF 업종 구성은 증권사 앱 ETF 정보·네이버 증권 ETF 분석에서 볼 수 있음(S2 화면) — 글 c04
- 계좌·세금 차이는 #245(S5)로 — 글 c04
- 사라·팔라는 쓰지 않음

## 누구라면
- SCHD를 이미 미국 계좌에 가진 사람이 국내 상장 4종을 더하는 경우: 업종·종목·환율 다 같음(c03)
- 국내 4종 가운데 둘을 같이 가진 사람: 1년 수익률 차이 0.4%p 안(c03, 4종끼리)
- 받는 달이 중요한 사람: SCHD 분기 4번, 국내 4종 올해 10~11번(c04)

## 함정
- '미국 상품과 한국 상품이니 나눠 담았다'는 생각 — 지수·업종·종목이 같고, TIGER는 환헤지도 안 해서 환율도 같이 탐(S2)
- '수익률이 다르게 보이니 다른 상품' — 달러 수익률과 원화 수익률을 맞대면 환율이 끼어듦(경쟁 3 sin1735). 우리는 국내 4종끼리 원화로만 비교

## 우리만
- SCHD 보유 102줄을 업종별로 더해 국내 4종과 업종 10개를 같은 날(11/13)로 맞댐 — 업종별 최대 차 0.29%p(IT), 세 업종 합 SCHD 54.09 / 국내 53.53~53.66(calc_out.txt) · 경쟁 8편 0편
- 국내 4종 상위 10종목(주식 수)이 SCHD 보유에 10/10 · 국내 4종 1년 NAV 수익률 차 0.37%p

## 예외
- 국내 4종 업종 비중은 네이버 증권 분류(sectorPortfolioList), SCHD는 슈왑 파일 Sector 칸을 같은 이름으로 맞춤 — 분류 출처가 달라 소수점 차이 일부는 분류 차이일 수 있음
- 1년 수익률은 국내 4종만(순자산가치 기준, 네이버 계산) — SCHD 달러 수익률은 환율 때문에 같은 표에 넣지 않음
- 국내 상위 10종목은 '주식 수' 순(네이버 표), 비중 순이 아님

## 한계
- 국내 4종의 종목별 비중 원본(운용사 PDF)은 11/17 못 받음 — 미래에셋 구성종목 ajax가 빈 값({"rtnData":[]}), 종목 겹침은 네이버 상위 10종목 이름으로만 셈
- SOL·ACE·KODEX의 환헤지 여부는 S3 요약문에 문구 없음 → 글은 TIGER만 '환헤지 안 함'으로 씀
- 업종이 왜 세 곳에 몰렸는지 지수 방법론 원문 안 읽음
- ISA·연금저축 담기 규칙은 이번에 원문(조세특례제한법 제91조의18)을 다시 못 받음(law.go.kr 웹 받기 실패) → 본문에 규칙을 쓰지 않고 #245로 넘김

## 대조
| 글 값 | 원문 값 | 출처 |
|---|---|---|
| 다섯 상품 같은 지수 'Dow Jones U.S. Dividend 100' | etfBaseIndex 'Dow Jones U.S. Dividend 100 Price Return Index' 4종 · SCHD 상품 페이지 | S2 https://m.stock.naver.com/api/stock/458730/etfAnalysis · S1 https://www.schwabassetmanagement.com/products/schd |
| 10년 넘게 배당을 준 미국 회사 중 재무 탄탄한 100곳 | ACE '10년 연속 배당금을 지급한 미국상장 종목 중 우량 펀더멘털 … 상위 100종' | S3 https://m.stock.naver.com/api/stock/402970/etfAnalysis |
| SCHD 보유 종목 102줄, 11월 13일 기준 | As-Of-Date 2026-11-13, 102줄 | S1 https://www.schwabassetmanagement.com/products/schd |
| 국내 4종이 주식 수로 가장 많이 담은 10종목 포드·컴캐스트·버라이즌, 열 곳 모두 SCHD에도 | etfTop10MajorConstituentAssets 4종 같음 · SCHD 파일에 10/10 | S2 https://m.stock.naver.com/api/stock/458730/etfAnalysis · S1 · calc_out.txt |
| 필수소비재 SCHD 20.4%, 국내 4종 20.1~20.2% | 20.39 / 20.11~20.16 | S1 · S2 https://m.stock.naver.com/api/stock/458730/etfAnalysis · calc_out.txt |
| 세 업종 합 SCHD 54.1%, 국내 53.5~53.7% | 54.09 / 53.53~53.66 | S1 · S3 https://m.stock.naver.com/api/stock/446720/etfAnalysis · calc_out.txt |
| 업종 10개 모두 차이 0.3%p 안, 가장 큰 IT 0.29%p | 업종별 최대 차 IT 12.10 vs 12.35~12.39 → 0.29 | S1 · S2 · calc_out.txt |
| 국내 4종 1년 수익률 23.4~23.7%, 차이 0.4%p 안 | navPerformanceList Y1 ACE 23.55·SOL 23.37·TIGER 23.42·KODEX 23.74 (차 0.37) | S2 https://m.stock.naver.com/api/stock/458730/etfAnalysis · S3 https://m.stock.naver.com/api/stock/489250/etfAnalysis |
| TIGER 환헤지 안 함, 원화로 바꾼 지수 수익률 따라감 | etfSummary '환헤지를 하지 않으므로 기초지수의 원화환산 수익률에 연동' | S2 https://m.stock.naver.com/api/stock/458730/etfAnalysis |
| SCHD 지난 1년 3·6·9·12월 네 번 | 분배 2025-12·2026-03·06·09 | S4 https://query1.finance.yahoo.com/v8/finance/chart/SCHD?range=1y&interval=1mo&events=div |
| 국내 4종 올해 10~11번 분배 | dividendCountThisYear TIGER·SOL 10, ACE·KODEX 11 | S2 · S3 https://m.stock.naver.com/api/stock/402970/etfAnalysis |
| 총보수 SCHD 0.06%, 국내 4종 0.01% 안팎 | Total Expense Ratio 0.060% · totalFee 0.01(KODEX 0.0099) | S1 https://www.schwabassetmanagement.com/products/schd · S3 https://m.stock.naver.com/api/stock/489250/etfAnalysis |
| 계좌·세금 차이는 #245 | 파이어맵 카페 글 | S5 https://cafe.naver.com/firemap/245 |

# 올리기 전 확인
- 2026-11-17 07:2x firemap-write(발행 당일 — 분배금 숫자는 '횟수'만 씀, 금액 안 씀)
- 다시 연 주소: https://www.schwabassetmanagement.com/products/schd (보유 파일 다시 받음) · https://m.stock.naver.com/api/stock/458730/etfAnalysis · https://m.stock.naver.com/api/stock/446720/etfAnalysis · https://m.stock.naver.com/api/stock/402970/etfAnalysis · https://m.stock.naver.com/api/stock/489250/etfAnalysis · https://query1.finance.yahoo.com/v8/finance/chart/SCHD?range=1y&interval=1mo&events=div · https://cafe.naver.com/firemap/245
- 기준일: 업종 비중 2026-11-13(SCHD 슈왑 As-Of · 네이버 기준) · 1년 수익률 2026-11-13 · 조회 2026-11-17
- 바뀐 것: 쇼츠(11/13 네이버) 국내 4종 세 업종 합 53.32~53.56% → 11/17 받은 값(기준 11/13) 53.53~53.66%, 에너지 14.69~14.76 → 14.94~14.97 · SCHD 세 업종 합 55.0%(10/15 보유) → 54.09%(11/13 보유) — 쇼츠 '절반 넘게'는 그대로 맞음
- 새로 찾은 것: SCHD 11/13 보유로 업종 10개 맞댐(최대 차 0.29%p) · 국내 4종 1년 수익률 차 0.37%p · 국내 상위 10종목 SCHD에 10/10
- 22:40 발행 회차: 쇼츠 yX3f9ESewcg 공개(19:20) 확인 뒤 발행, 네이버 기준일이 11/14 이후로 바뀌었으면 calc.py 다시 돌려 숫자 확인
