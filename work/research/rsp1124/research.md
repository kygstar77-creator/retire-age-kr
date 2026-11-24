# rsp1124 자료조사 (카페 지수 비축, firemap-write-b 11/22 13:4x 회차) — S&P500 동일가중(RSP) vs 시가총액 가중(SPY), 직접 계산형

## 검증
- 수요: kwvol 11/22 — RSP 680 · 동일가중ETF 270 · S&P500동일가중 150 (검색어 자체는 작음) · 대신 toprank 'S&P500 동일가중' 상위 8편 중 6편이 2주 안 글(11/22) — 요즘 묻는 주제 · SCHD·DGRO(52,000·2,420)는 schdpair1105와 겹쳐 뺌
- 경쟁에서 터진 증거: toprank 1위 annalife_ 댓글 3 · 7위 tjfdydghks12 댓글 3 · 6편 모두 11월 글
- 겹침: 우리 spx10y1122(S&P500 하나 보유 기간별 손해 비율)·ndxspx1118(나스닥100 vs S&P 하락장)·#413(S&P500 분배금) — 동일가중을 다룬 우리 글 0편 · 축 순서는 회의가 칸 배정 때 정함
- 칸: 비축(slots.json reserve cafe, 범위 안 비축 0~1 · 최소 2) — slot.txt 2026-11-24 16(지수 칸 후보), 회의가 옮김

## 원문
- S1 야후 파이낸스 chart API RSP·SPY 일별 종가·수정 종가·분배 events 2003-05-01~2026-11-20, 11/22 13:4x 받음(raw/RSP.json·raw/SPY.json, fetch.py): https://query1.finance.yahoo.com/v8/finance/chart/RSP · https://query1.finance.yahoo.com/v8/finance/chart/SPY
- S2 인베스코 RSP 상품 페이지(Total expense ratio 0.20%, "rebalanced quarterly", Inception 04/24/2003, holdings 505 as of 11/19/2026), 11/22 받음(raw/invesco_rsp.txt, fetch_pw.py): https://www.invesco.com/us/en/etf/sp-500-equal-weight-rsp.html
- S3 스테이트 스트리트 SPY 상품 페이지(Gross Expense Ratio 0.0945%), 11/22 받음(raw/ssga_spy.html): https://www.ssga.com/us/en/intermediary/etfs/state-street-spdr-sp-500-etf-trust-spy
- S4 스테이트 스트리트 SPY 보유 종목 파일 As of 19-Nov-2026(상위 10개 합 36.9%), 11/22 받음(raw/spy_holdings_1119.xlsx): https://www.ssga.com/us/en/intermediary/library-content/products/fund-data/etfs/us/holdings-daily-us-en-spy.xlsx
- S5 미래에셋 TIGER 미국S&P500동일가중(488500) 상품 페이지(총보수 0.2%·분기 리밸런싱·환헤지 안 함·1년 기준가격 7.78%, 2026.11.20 기준), 11/22 받음(raw/tiger_488500.txt): https://investments.miraeasset.com/tigeretf/ko/product/search/detail/index.do?ksdFund=KR7488500000
- S6 미래에셋 TIGER 미국S&P500(360750) 상품 페이지(총보수 0.0068%·1년 기준가격 1.78%), 11/22 받음(raw/tiger_360750.txt): https://investments.miraeasset.com/tigeretf/ko/product/search/detail/index.do?ksdFund=KR7360750004
- S7 S1으로 직접 계산(calc.py → calc_out.txt) — 보유 기간별 앞선 비율·해마다 차이·낙폭·회복

## 경쟁
- toprank.txt('S&P500 동일가중' 블로그 상위 8, 11/22). 본문 6편 bench_raw(bench_fetch.py). 5(read_sijang) 2003년 이후 연환산 11.29% vs 11.35%·상위 10개 40.7%(2025년 말), 4(arpha1) 2022년만 이김·2023·2024 12%p 넘게 뒤짐, 1(annalife_) 뜻·국내 TIGER 1년 5.68%(시장가격·분배 제외), 2·6(goldmoneyissue) 비중 차이 설명, 7(tjfdydghks12) 상품 소개 전부. 거래일마다 사서 N년 들고 있었을 때 앞선 비율·회복 달 수를 센 글 0편 → bench.md

## 질문
1. 지금 동일가중으로 갈아타야 하나 — https://blog.naver.com/arpha1/224475618072 ('S&P500 동일가중으로 갈아타야 할까') → 답: 아무 날 사서 1~10년 들고 있었을 때 앞선 경우 44~46%, 23년 연평균은 11.0% vs 10.9% — 권유 안 하고 숫자만
2. 같은 500개인데 왜 수익률이 다르나 — https://blog.naver.com/goldmoneyissue/224485160971 ('같은 종목인데 수익률이 다른 이유') → 답: 비중(상위 10개 36.9% vs 회사마다 0.2% 정도), 석 달마다 다시 맞춤
3. 하락장에 덜 빠지나 — https://blog.naver.com/neighbormrbear/224475055748 ('대형 기술주 쏠림이 부담된다면?') → 답: 세 번 중 2022년만 덜 빠짐, 2008년엔 더 빠졌지만 회복은 43달 vs 58달로 빨랐음
4. 국내에서 사려면 — https://blog.naver.com/annalife_/224486045247 ('TIGER 미국S&P500동일가중') → 답: 488500, 총보수 0.2%, 환헤지 안 함, 1년 기준가격 7.78% vs TIGER 미국S&P500 1.78%

## 왜
- 왜 수익이 갈리나: 담는 비중이 다름(S2·S4) — 큰 회사가 많이 오른 해엔 SPY가, 아닌 해엔 동일가중이 앞섬(해마다 차이 S7)
- 왜 23년 연평균은 같은데 앞선 날은 절반이 안 되나: 이긴 해 차이가 컸음(2009 +18.3%p) — 계산으로 보인 것, 원문에 이유 설명은 없음
- 왜 2022년엔 덜 빠졌나: 원문(S1~S6)에 이유 없음 — 안 씀(금리 인상기라는 시기 이름만)

## 그래서
- 동일가중을 고르는 건 '늘 이기는 쪽'이 아니라 '큰 회사 쏠림을 줄이는 쪽'을 고르는 것 — 숫자는 반반에 조금 못 미침
- 국내 계좌면 보수 차이(0.2% vs 0.0068%)와 환헤지 여부를 같이 봄
- 1년 수익률 하나로 판단하지 않음 — 기간 따라 순서가 뒤집힘

## 누구라면
- 이미 S&P500 ETF만 있는 사람: 빅테크 쏠림(상위 10개 36.9%)이 걱정이면 동일가중이 다른 선택지 — 다만 2008·2020엔 더 빠짐
- 10년 넘게 둘 사람: 10년 보유에서도 앞선 경우 46%, 누적 차이 중간값 −10%p
- 국내 계좌(ISA·연금저축)로 사는 사람: 488500, 환헤지 안 함 — 원화 수익은 달러 가격 따라 달라짐

## 함정
- '동일가중은 하락장에 덜 빠진다'는 반만 맞음 — 2008·2020엔 더 빠짐
- 1년 수익률만 보고 고르기 — 올해 동일가중 +9.6% vs +1.9%이지만 2023·2024엔 12%p 넘게 뒤짐
- 보수 — 국내 동일가중 0.2%는 TIGER 미국S&P500 0.0068%의 약 30배

## 한계
- 세전·달러 기준, 분배금 재투자 가정 — 세금·환율·매매 수수료 안 뺌
- 야후 수정 종가(2차 가공 값) — 운용사 공식 장기 수익률 표와 소수점 차이 있을 수 있음(경쟁 5의 11.29%·11.35%와 우리 11.0%·10.9%는 기간 끝날이 다름)
- 국내 488500은 상장 2024-07-23라 장기 셈 불가 — 1년은 운용사 표(S5·S6) 값 그대로
- 2003년 이후만 — 닷컴 버블(2000~02)은 RSP 상장 전이라 없음
- S&P 다우존스 지수 공식 페이지는 안 엶(지난 spx10y1122 때 403)

## 대조
| 글 값 | 원문 값 | 출처 |
|---|---|---|
| 5년 보유 앞선 45% · 1년 44% · 3년 45% · 10년 46% · 시작일 5,679개 | 45 · 44 · 45 · 46 · 5,679 | S1·S7 calc_out.txt https://query1.finance.yahoo.com/v8/finance/chart/RSP |
| 10년 보유 누적 차이 중간값 10%p 뒤짐 | −10.0%p | S1·S7 calc_out.txt https://query1.finance.yahoo.com/v8/finance/chart/SPY |
| 23년 연평균 11.1% vs 11.1% | 11.1 · 11.1 | S1·S7 calc_out.txt https://query1.finance.yahoo.com/v8/finance/chart/RSP |
| 22해 중 10해 · 2009 +18.3%p · 2022 +6.6%p · 2023·2024 12%p 넘게 뒤짐 | 10 · 18.3 · 6.6 · −12.5 · −12.1 | S1·S7 calc_out.txt https://query1.finance.yahoo.com/v8/finance/chart/RSP |
| 올해 12.4% vs 6.7%(11/23) | 12.4 · 6.7 | S1·S7 calc_out.txt https://query1.finance.yahoo.com/v8/finance/chart/SPY |
| 낙폭 2008 59.9·55.2 · 2020 39.0·33.7 · 2022 21.4·24.5 | 같음 | S1·S7 calc_out.txt https://query1.finance.yahoo.com/v8/finance/chart/RSP |
| 회복 43·58달 · 9·6달 · 25·23달 | 같음 | S1·S7 calc_out.txt https://query1.finance.yahoo.com/v8/finance/chart/SPY |
| 상위 10개 36.4%(11/20) | 36.4 | S4 https://www.ssga.com/us/en/intermediary/library-content/products/fund-data/etfs/us/holdings-daily-us-en-spy.xlsx |
| RSP 보수 0.20%·석 달마다 다시 맞춤 · 0.2% 정도씩 | 0.20% · quarterly · 505종목 | S2 https://www.invesco.com/us/en/etf/sp-500-equal-weight-rsp.html |
| SPY 보수 0.0945% | 0.0945% | S3 https://www.ssga.com/us/en/intermediary/etfs/state-street-spdr-sp-500-etf-trust-spy |
| 488500 총보수 0.2% · 환헤지 안 함 · 1년 4.96%(11/24 기준) | 0.2 · 환헤지를 하지 아니함 · 4.96 | S5 https://investments.miraeasset.com/tigeretf/ko/product/search/detail/index.do?ksdFund=KR7488500000 |
| TIGER 미국S&P500 총보수 0.0068% · 1년 -2.80%(11/24 기준) | 0.0068 · -2.80 | S6 https://investments.miraeasset.com/tigeretf/ko/product/search/detail/index.do?ksdFund=KR7360750004 |
| 보수 약 30배 | 0.2 ÷ 0.0068 = 29.4 | S5·S6 https://investments.miraeasset.com/tigeretf/ko/product/search/detail/index.do?ksdFund=KR7360750004 |
| 일반 계좌 분배금·매매차익 배당소득세 15.4% | 과세내용 15.4% | S5 https://investments.miraeasset.com/tigeretf/ko/product/search/detail/index.do?ksdFund=KR7488500000 |
| TIGER 미국S&P500도 환헤지 안 함 | 환헤지를 하지 않으므로 | S6 https://investments.miraeasset.com/tigeretf/ko/product/search/detail/index.do?ksdFund=KR7360750004 |
| 상위 8편 모두 이번 달(11월) 글 | 8/8 (11.22·1일 전·2일 전·2주 전) | toprank.txt(네이버 블로그 탭 11/22) https://blog.naver.com/annalife_/224486045247 |

# 올리기 전 확인
- 2026-11-24 15:4x firemap-write(발행 날) — 대조 출처 전부 다시 엶
- 다시 연 주소: https://query1.finance.yahoo.com/v8/finance/chart/RSP · https://query1.finance.yahoo.com/v8/finance/chart/SPY · https://www.invesco.com/us/en/etf/sp-500-equal-weight-rsp.html · https://www.ssga.com/us/en/intermediary/etfs/state-street-spdr-sp-500-etf-trust-spy · https://www.ssga.com/us/en/intermediary/library-content/products/fund-data/etfs/us/holdings-daily-us-en-spy.xlsx · https://investments.miraeasset.com/tigeretf/ko/product/search/detail/index.do?ksdFund=KR7488500000 · https://investments.miraeasset.com/tigeretf/ko/product/search/detail/index.do?ksdFund=KR7360750004 · https://blog.naver.com/annalife_/224486045247 (모두 11/24)
- 기준일: 2026-11-23 종가(미국) · 국내 기준가격 2026.11.24 · SPY 보유 종목 2026-11-20
- 바뀐 것: 기준일 11/20→11/23(SPY 11/23 하루 +4.7%) · 상장 뒤 연평균 RSP 11.0→11.1%·SPY 10.9→11.1% · 올해 RSP 9.6→12.4%·SPY 1.9→6.7% · 1년 보유 시작일 5,678→5,679(비율 44% 그대로) · 국내 1년 488500 7.78→4.96%·360750 1.78→-2.80% · SPY 상위 10개 36.9→36.4%(11/20자) · 보수·리밸런싱·하락장·연도별·보유 기간 비율 그대로
- 새로 찾은 것: 23년 통째 연평균이 11/23 반등으로 둘 다 11.1% — 누적은 SPY +1105%가 RSP +1098%를 다시 앞섬(11/20엔 RSP 앞섬) · 거래일마다 사서 1~10년 보유 시 동일가중 앞선 비율 44~46% · 2008년 회복 43달 vs 58달
- 조사 뒤 공표: data/release_calendar.json — 가격 매일, RSP·SPY 12월 분배(12월 셋째 주 전후) · 488500 분기 리밸런싱 12월

# 올리기 전 확인(11/22 조사 날 기록)
- 2026-11-22 13:5x firemap-write-b(조사·작성 날, 비축 — 발행 회차가 야후·운용사 페이지 다시 받아 그날 종가·기준가격으로 갱신)
- 다시 연 주소: https://query1.finance.yahoo.com/v8/finance/chart/RSP · https://query1.finance.yahoo.com/v8/finance/chart/SPY · https://www.invesco.com/us/en/etf/sp-500-equal-weight-rsp.html · https://www.ssga.com/us/en/intermediary/etfs/state-street-spdr-sp-500-etf-trust-spy · https://www.ssga.com/us/en/intermediary/library-content/products/fund-data/etfs/us/holdings-daily-us-en-spy.xlsx · https://investments.miraeasset.com/tigeretf/ko/product/search/detail/index.do?ksdFund=KR7488500000 · https://investments.miraeasset.com/tigeretf/ko/product/search/detail/index.do?ksdFund=KR7360750004 · https://blog.naver.com/annalife_/224486045247 (모두 11/22)
- 기준일: 2026-11-20 종가(미국) · 국내 기준가격 2026.11.20 · SPY 보유 종목 2026-11-19
- 바뀐 것: 처음 조사(11/22) — 기준일 2026-11-20 · 올해 RSP 9.6%·SPY 1.9% · 국내 1년 7.78%·1.78% · 발행 날 회차가 calc.py·운용사 페이지 다시 받아 이 줄을 그날 숫자로 고친다(1일 안)
- 새로 찾은 것: 거래일마다 사서 1~10년 보유 시 동일가중 앞선 비율 44~46% · 2008년 더 빠졌지만 회복은 43달 vs 58달 · 경쟁 글 이 셈 0편
- 조사 뒤 공표: data/release_calendar.json — 가격 매일, RSP·SPY 12월 분배(12월 셋째 주 전후) · 488500 분기 리밸런싱 12월
