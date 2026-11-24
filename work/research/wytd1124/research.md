# wytd1124 자료조사 (카페 11/24 18:40 칸, firemap-write 11/23 07:1x 회차 — 운영실장 07:10 지시) — 지수 올해 성적 원화 환산, 통계·기록형

## 검증
- 수요: kwvol 11/23 — S&P500 296,900 · 나스닥100 282,500 · 코스피200 167,500 · 니케이225 69,510 · 세계증시 42,080 · 미국지수 20,300 · 유로스톡스50 19,170
- 경쟁에서 터진 증거: toprank 'S&P500 환율 수익률' 상위 8편 중 1·2위가 11/23, 나머지 3일~2주 안 — 지금 계속 쓰이는 주제(원화 강세로 계좌 수익률이 지수와 다르다는 글)
- 겹침: 11/24 10:10 dow1124(다우 비중)·16:10 rsp1124(S&P500 동일가중 장기 수익)·11:30 KOSPI-1(코스피 하루 -5% 23번)과 다른 각도(올해 다섯 지수 원화 환산) · 10/14 r1cafe_fx1014(미국 ETF 환차손 1년)는 S&P500 하나·한 달 넘게 전 · 11/23 santa1123(나스닥100 12월)과 다름
- 축 배분: 11/24 배당(07:40)→지수(10:10)→부동산(12:40)→지수(16:10)→지수(18:40 이 글)→배당(22:40) — 지수 2칸 연달아지만 대상·각도 다름(동일가중 장기 vs 올해 원화)

## 원문
- S1 야후 파이낸스 chart API 일봉 ^GSPC·^NDX·^KS11·^N225·^STOXX50E·^SP500TR, 11/23 받음(raw/): https://query1.finance.yahoo.com/v8/finance/chart/%5EGSPC · https://query1.finance.yahoo.com/v8/finance/chart/%5ENDX · https://query1.finance.yahoo.com/v8/finance/chart/%5EKS11 · https://query1.finance.yahoo.com/v8/finance/chart/%5EN225 · https://query1.finance.yahoo.com/v8/finance/chart/%5ESTOXX50E · https://query1.finance.yahoo.com/v8/finance/chart/%5ESP500TR
- S2 세인트루이스 연준 FRED SP500·NASDAQ100·NIKKEI225(야후 값 대조), 11/23: https://fred.stlouisfed.org/series/SP500 · https://fred.stlouisfed.org/series/NASDAQ100 · https://fred.stlouisfed.org/series/NIKKEI225
- S3 한국은행 ECOS 731Y001 주요국 통화 대원화 환율(매매기준율, 일), 11/23: https://ecos.bok.or.kr/ (StatisticSearch 731Y001/D 0000001·0000002·0000003)
- S4 한국은행 ECOS 802Y001 KOSPI지수(일, 야후 대조), 11/23: https://ecos.bok.or.kr/ (StatisticSearch 802Y001/D 0001000)
- S5 S1·S3로 직접 계산(calc.py → calc_out.txt)

## 경쟁
- toprank.txt('S&P500 환율 수익률' 블로그 상위 8, 11/23). 본문 5편 bench_raw. 1(winnerking) 환율 1,300원 가정 계산표, 2(spmj9) KODEX 미국S&P500 vs SPY 6개월, 3(todaybotaem) 환헤지·환노출 가정 10%, 4(sjxmfdl) 퇴직연금 환헤지 뉴스 요약, 5(joyuldrama) S&P500 10년 3.6배 vs 원화 4.2배. 다섯 지수 올해 실제 원화 성적·한국은행 매매기준율로 센 글 0편 → bench.md

## 질문
1. 지수는 올랐는데 내 계좌는 왜 손해인가 — https://blog.naver.com/winnerking/224475984112 ('미국 지수는 올랐는데 내 계좌 수익률은 그만큼 오르지 않았더군요') → 답: 원화가 강해져 달러가 6.8% 싸짐, S&P500 +5.7%가 원화로 -1.5%(11/23 기준)
2. 같은 S&P500 ETF인데 수익률이 왜 다른가 — https://blog.naver.com/sjxmfdl/224484285817 ('같은 S&P500 ETF인데 수익률 차이 발생') → 답: 환율 변화가 곱해짐(배당 넣은 토탈리턴도 달러 +2.0%·원화 -5.4%) — 환헤지 상품 비교는 이 글에서 안 다룸(한계)
3. 국내 상장 S&P500이 SPY보다 더 빠진 이유 — https://blog.naver.com/spmj9/224478725687 ('KODEX 미국S&P500 … 8.31% 하락') → 답: 원화 환산 차이, 다섯 지수 모두 원화로 다시 셈
4. 다른 나라 지수는 어땠나 — 연관검색어 세계증시 42,080·니케이225 69,510(kwvol 11/23, https://searchad.naver.com/) → 답: 원화로 플러스는 코스피 +11.7%·닛케이 +3.0%뿐, 유로스톡스50은 -8.8%로 꼴찌(11/23 기준)

## 왜
- 왜 원화로 손해인가: 원화 수익률 = (1+지수 수익률)×(끝 환율÷처음 환율)−1 — 달러 1,434.9→1,330.8원(S3)
- 왜 유로스톡스50이 꼴찌로 내려가나: 유로가 13.4%로 가장 많이 싸짐(S3)
- 왜 코스피는 그대로인가: 원화 지수라 환율 영향 없음

## 그래서
- 해외 지수 투자 성적을 볼 때 지수 등락과 환율 변화를 같이 봐야 함
- 같은 해에도 산 시점에 따라 성적이 크게 갈림(코스피 6월 최고치 대비 -46.6%)

## 누구라면
- 연금저축·ISA로 국내 상장 미국 지수 ETF(환노출)를 가진 사람: 지수 +1%여도 원화 계좌는 손해일 수 있음
- 해외 지수를 나라별로 나눠 담은 사람: 원화로 바꾸면 순위가 바뀜
- 코스피 지수 ETF를 6월에 산 사람: 연초 산 사람과 성적이 정반대

## 함정
- 뉴스의 '올해 S&P500 +1%'를 내 원화 계좌 수익률로 착각
- 가격 지수(배당 뺌)와 토탈리턴을 섞어 비교
- 원화 환산은 환전 수수료·세금·보수를 뺀 단순 계산 — 실제 ETF 수익률과 다름

## 한계
- 국내 상장 ETF(환노출·환헤지) 실제 가격은 안 셈, (H) 설명은 운용사 원문 대신 2차 2곳 — 국내 ETF 11/20 종가는 미국 11/19 종가를 반영해 날짜가 어긋남
- 지수 종가와 한국은행 매매기준율은 시각이 다름(매매기준율은 한국 시간 낮 기준) — 하루 안팎 오차
- 닛케이·유로스톡스·코스피는 2025-12-30이 마지막 거래일이지만 환율은 다섯 지수 모두 2025-12-31 매매기준율로 통일(본문·그림과 같게, 12-30 환율이면 닛케이 +1.7%·유로스톡스 -11.4%)
- 유로스톡스50은 FRED 대조 없음(야후 하나) — ECOS 원화 환율만 1차

## 대조
| 글 값 | 원문 값 | 출처 |
|---|---|---|
| S&P500 +5.7% · 원화 -1.5% | 6,845.50 → 7,237.17(11/23) · ×1337.3/1434.9 | S1 https://query1.finance.yahoo.com/v8/finance/chart/%5EGSPC · S2 https://fred.stlouisfed.org/series/SP500 · S3 |
| 나스닥100 +5.9% · 원화 -1.3% | 25,249.85 → 26,746.10(11/23) | S1 https://query1.finance.yahoo.com/v8/finance/chart/%5ENDX · https://api.nasdaq.com/api/quote/NDX/info?assetclass=index (11/23 26,746.10 +6.86% 같음) |
| 닛케이225 +12.1% · 원화 +3.0% (11/23 일본 휴장 → 11/20 종가) | 50,339.48 → 56,436.65 · ×842.95/917.63 | S1 https://query1.finance.yahoo.com/v8/finance/chart/%5EN225 · S2 https://fred.stlouisfed.org/series/NIKKEI225 |
| 유로스톡스50 +4.8% · 원화 -8.8% | 5,796.22 → 6,074.47(11/23) · ×1467.69/1685.72 | S1 https://query1.finance.yahoo.com/v8/finance/chart/%5ESTOXX50E · S3 https://ecos.bok.or.kr/ |
| 코스피 +11.7% | 4,214.17 → 4,708.54(11/23) | S4 https://ecos.bok.or.kr/ · S1 https://query1.finance.yahoo.com/v8/finance/chart/%5EKS11 |
| 달러 1,434.9 → 1,337.3원 · 6.8% 내림 · 엔 8.1% · 유로 12.9% | 1434.9·1337.3 · 917.63→842.95 · 1685.72→1467.69 (11/23) | S3 https://ecos.bok.or.kr/ |
| S&P500 토탈리턴 달러 +6.8% · 원화 -0.5% | 15,220.45 → 16,256.40(11/23) | S1 https://query1.finance.yahoo.com/v8/finance/chart/%5ESP500TR · S5 calc_out.txt |
| S&P500 10월 6일 최고치보다 7.4% 낮음 · 11월 23일 하루 4.7% 오름 | 7,818.93 · 6,910.39(11/20) → 7,237.17(11/23) | S1 https://query1.finance.yahoo.com/v8/finance/chart/%5EGSPC · S2 https://fred.stlouisfed.org/series/SP500 |
| 코스피 6월 22일 9,114.55 · 11월 23일 4,708.54 · 48.3% 낮음 | 9114.55 · 4708.54 | S4 https://ecos.bok.or.kr/ · S1 https://query1.finance.yahoo.com/v8/finance/chart/%5EKS11 |
| 닛케이225 6월 25일 최고치보다 22.0% 낮음 | 72,366.34 → 56,436.65 | S1 https://query1.finance.yahoo.com/v8/finance/chart/%5EN225 |
| 지수 변화에 환율 변화를 곱함 · 1달러어치가 1.057달러 | 1.0572×(1337.3/1434.9)−1 = −1.47% | S5 calc_out.txt https://ecos.bok.or.kr/ |
| (H) 없는 환노출형은 환율 변화를 그대로 · 환헤지형은 환율 영향을 줄이도록 만든 상품(2차) | '환헤지형은 이러한 환율 영향을 줄이도록 설계'·'헤지 비용과 운용 차이' · KB자산운용 설명 (H) | 2차 https://blog.naver.com/todaybotaem/224471185033 · https://blog.naver.com/joyuldrama/224469529724 |

# 올리기 전 확인
- 2026-11-23 07:2x firemap-write(조사·작성 날 — 발행 회차가 야후·ECOS 다시 받아 calc.py 다시 돌림, 11/23 미국 종가가 나오면 기준일을 바꿀지 그날 정함)
- 다시 연 주소: https://query1.finance.yahoo.com/v8/finance/chart/%5EGSPC · https://query1.finance.yahoo.com/v8/finance/chart/%5ENDX · https://query1.finance.yahoo.com/v8/finance/chart/%5EKS11 · https://query1.finance.yahoo.com/v8/finance/chart/%5EN225 · https://query1.finance.yahoo.com/v8/finance/chart/%5ESTOXX50E · https://query1.finance.yahoo.com/v8/finance/chart/%5ESP500TR · https://fred.stlouisfed.org/series/SP500 · https://fred.stlouisfed.org/series/NASDAQ100 · https://fred.stlouisfed.org/series/NIKKEI225 · https://ecos.bok.or.kr/ · https://blog.naver.com/todaybotaem/224471185033 · https://blog.naver.com/joyuldrama/224469529724
- 기준일: 2026-11-20 종가·매매기준율
- 바뀐 것: 처음 조사(11/23) — 기준일 2026-11-20 · S&P500 +1.0%·원화 -6.4%·달러 -7.3% · 발행 날 회차가 calc.py 다시 돌려 이 줄을 그날 숫자로 고친다(1일 안)
- 새로 찾은 것: 다섯 지수 원화 순위 뒤바뀜(유로스톡스50 현지 3위 → 원화 꼴찌) · 코스피 6월 최고치 대비 -46.6% · 경쟁 글 다섯 지수 실제 원화 성적 0편
- 조사 뒤 공표: data/release_calendar.json — 지수 종가 매 거래일, 매매기준율 매 영업일
- 2026-11-24 18:3x firemap-write 발행 회차 — 야후(^GSPC·^NDX·^KS11·^N225·^STOXX50E·^SP500TR) 다시 받음(fetch.py), ECOS 731Y001 11/23 매매기준율·802Y001 KOSPI 11/23 다시 받음
- 다시 연 주소: https://query1.finance.yahoo.com/v8/finance/chart/%5EGSPC · https://query1.finance.yahoo.com/v8/finance/chart/%5ENDX · https://query1.finance.yahoo.com/v8/finance/chart/%5EKS11 · https://query1.finance.yahoo.com/v8/finance/chart/%5EN225 · https://query1.finance.yahoo.com/v8/finance/chart/%5ESTOXX50E · https://query1.finance.yahoo.com/v8/finance/chart/%5ESP500TR · https://ecos.bok.or.kr/ · https://fred.stlouisfed.org/series/SP500 · https://fred.stlouisfed.org/series/NASDAQ100 · https://fred.stlouisfed.org/series/NIKKEI225 · https://blog.naver.com/todaybotaem/224471185033 · https://blog.naver.com/joyuldrama/224469529724
- 기준일: 2026-11-23 종가·매매기준율(닛케이225는 11/23 일본 휴장이라 11/20 종가)
- 바뀐 것: 11/23 미국장 S&P500 하루 +4.7%(6,910.39→7,237.17)로 결론 숫자가 바뀜 → S&P500 달러 +1.0%→+5.7%·원화 -6.4%→-1.5% · 달러 1,330.8→1,337.3원(7.3%→6.8% 싸짐) · 코스피 +15.6%→+11.7%·최고 대비 46.6%→48.3% · 현지 1위가 코스피→닛케이225로 바뀌어 c03 '순위' 문단을 '유로스톡스50 현지 꼴찌→원화 꼴찌·닛케이 1→2등'으로 고침 · 그림 3장 다시(mkimg.py) · 11/20 판은 calc_out_1120.txt·pkg.bak1120
- 새로 찾은 것: S&P500 11/23 하루 +4.7% · 11/23 일본 휴장(닛케이 마지막 11/20)
- 조사 뒤 공표: data/release_calendar.json — 지수 종가 매 거래일, 매매기준율 매 영업일
