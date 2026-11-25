# lev1125 자료조사 (카페 지수 칸 11/25 16:10, firemap-write-b 11/23 16:4x 회차) — 나스닥100 레버리지 QLD·TQQQ, 지수 제자리일 때 직접 계산형

## 검증
- 수요: kwvol 11/23 — QLD 76,900 · TQQQ 56,900 · 나스닥100 282,500 · 나스닥100레버리지 360 · 우리 카페 제목 QLD·TQQQ 0편(블로그 levetf·qld0925는 9월, 카페 lev2x1018은 단일종목)
- 경쟁에서 터진 증거: toprank 'TQQQ 장기투자' 상위 8편 모두 2주 전 이후 글(11/23 두 편·1일 전 두 편) · yunsdaq 댓글 3 · 11/20 QQQ 하루 -5.67%·TQQQ -15.94% 뒤 묻는 글 늘어남
- 겹침: ndx1121(나스닥100 하락장 뒤)·ndxspx1118·ndxetf1122(나스닥100 ETF 네 곳)와 각도 다름 — 레버리지 상품을 다룬 우리 카페 글 0편 · 11/25 칸 축 지수(16:10)
- 칸: 11/25 16:10 TBD-지수(write-b) — slot.txt 2026-11-25 16

## 원문
- S1 야후 파이낸스 chart API QQQ·QLD·TQQQ 일별 수정 종가 2000~2026-11-20, 11/23 16:5x 받음(raw/*.json, fetch.py): https://query1.finance.yahoo.com/v8/finance/chart/QQQ · https://query1.finance.yahoo.com/v8/finance/chart/QLD · https://query1.finance.yahoo.com/v8/finance/chart/TQQQ
- S2 프로셰어즈 QLD 상품 페이지(2x daily · Net Expense Ratio 0.89% · Inception 6/19/06), 11/23 받음(raw/proshares_qld.html): https://www.proshares.com/our-etfs/leveraged-and-inverse/qld
- S3 프로셰어즈 TQQQ 상품 페이지(3x daily · Net 0.78% · 'higher index volatility contribute to returns worse than the Daily Target'), 11/23 받음(raw/proshares_tqqq.html): https://www.proshares.com/our-etfs/leveraged-and-inverse/tqqq
- S4 정책브리핑 금융위원회 해명 2026.06.26(해외상장 레버리지 신규 투자 기본예탁금 1천만원·사전교육·신용미수 제한), 11/23 받음(raw/a715f1ae.html): https://www.korea.kr/briefing/actuallyView.do?newsId=148967174
- S5 금융위원회 7/24 보도자료(3천만원·현금은 단일종목 한정), 11/23 받음(raw/fsc_87403.html): https://www.fsc.go.kr/po010102/87403
- S6 S1으로 직접 계산(calc.py → calc_out.txt)

## 경쟁
- toprank.txt('TQQQ 장기투자' 블로그 탭 상위 8, 11/23), 본문 6편 bench_raw. 1(flyfreedom29) 뜻·사전교육·QLD vs TQQQ 표·국내 상품, 2(mizugal) 가상 10% 예시로 음의 복리·연초 1천만원, 3(yunsdaq) 운용사 10년 38%·5년 11% 시작 시점, 5(mondayholdings) 2011·2018 보합 해 TQQQ 마이너스(해 단위), 6(todayisgood2) 2022 -79%. QQQ가 1년 제자리였던 시작일 전부(370번)를 세거나, 올해 6/2→10/6 지수 +2%에 TQQQ -3% 같은 실제 구간을 짚은 글 0편 → bench.md

## 질문
1. 횡보장에서 원금이 녹나 — https://blog.naver.com/mondayholdings/224470349959 ('레버리지는 횡보장에서 원금이 녹는다?') → 답: QQQ 1년 제자리 370번 중 TQQQ 손실 91%, ±1% 76번은 전부 손실
2. 장기로 들면 되나 — https://blog.naver.com/mizugal/224478927264 ('TQQQ 장기투자 월 100만원씩 가능할까') → 답: 길게 오르면 1억→약 201억이지만 2021 고점 회복 1,111일 — 권유 없이 양쪽 숫자
3. 왜 기간마다 수익률이 다른가 — https://blog.naver.com/yunsdaq/224471815686 ('10년 38%, 5년은 왜 11%일까') → 답: 하루 배수라 경로(오르내림)에 따라 갈림, 운용사 문장(S3)
4. 국내에서 사려면 — https://blog.naver.com/flyfreedom29/224486541790 ('거래 전 필수 확인 사항: 해외 레버리지 ETF 사전교육') → 답: 사전교육 + 기본예탁금 1천만원(S4), 신용·미수 제한

## 왜
- 왜 지수 제자리인데 손실인가: 하루마다 2·3배를 다시 맞춤 — 운용사 원문 'Smaller index gains/losses and higher index volatility contribute to returns worse than the Daily Target'(S3)
- 왜 6/2→10/6에 TQQQ가 내렸나: 그 사이 하루 2% 넘는 날 10일(S6) — 운용사가 말한 '변동성 큼' 조건, 그 이상 이유는 원문에 없음
- 왜 긴 상승장엔 3배 넘게 벌었나: 'Larger index gains/losses and lower index volatility contribute to returns better'(S3)

## 그래서
- 지수 방향만 보고 2·3배를 기대하면 안 됨 — 오르내림이 큰 제자리 구간은 손실 쪽으로 기움
- 들고 있으려면 회복 기간(2021 고점 1,111일)을 견딜 수 있는지 먼저 봄
- 국내 계좌면 사전교육·기본예탁금 1천만원을 먼저 갖춤(S4)

## 누구라면
- 이미 QQQ·국내 나스닥100 ETF가 있는 사람: 같은 지수라도 레버리지는 제자리 구간에서 따로 움직임 — 비교 숫자로 봄
- 처음 해외 레버리지를 사려는 사람: 사전교육·1천만원 조건(S4)
- 적립식으로 모으는 사람: 이 글은 한 번에 산 경우만 셈 — 적립식은 안 셈(한계)

## 함정
- '3배니까 지수가 오르면 3배'는 하루 기준일 뿐 — 6/2→10/6 지수 +2.0%에 TQQQ -3.0%
- 단일종목 3천만원 기사와 헷갈림 — QLD·TQQQ 같은 지수 레버리지는 1천만원(S4·S5)
- 고점 대비 -82%면 원금 되찾으려면 5배 넘게 올라야 함(1÷0.183=5.5)

## 한계
- 세전·달러, 분배 재투자 가정 — 세금·환율·매매 수수료 안 뺌
- 야후 수정 종가(2차 가공) — 운용사 NAV 수익률과 소수점 차이 가능
- 한 번에 산 경우만 — 적립식·리밸런싱은 안 셈
- 2000~02 닷컴 하락은 QLD·TQQQ 상장 전이라 없음
- 국내 상장 나스닥100 레버리지(합성) 상품 페이지는 안 엶 — 글에서 국내 상품 수익률은 안 씀

## 대조
| 글 값 | 원문 값 | 출처 |
|---|---|---|
| 2026년 QQQ 4.2% · QLD -1.8% · TQQQ -11.9% (11/24 종가) | 4.2 · -1.8 · -11.9 | S1·S6 calc_out.txt https://query1.finance.yahoo.com/v8/finance/chart/QQQ |
| 6/2→10/6 QQQ +2.0% · TQQQ -3.0% · QLD +0.3% · 2% 넘는 날 10일 | 2.0 · -3.0 · 0.3 · 10 | S1·S6 calc_out.txt https://query1.finance.yahoo.com/v8/finance/chart/TQQQ |
| 10월 6일 QQQ 올해 최고 · TQQQ 올해 최고 6월 2일 | 2026-10-06 · 2026-06-02 | S1·S6 calc_out.txt https://query1.finance.yahoo.com/v8/finance/chart/TQQQ |
| 사는 날 3,971번 중 370번 · TQQQ 가운데 -11.0% · 손실 91% | 3971 · 370 · -11.0 · 91 | S1·S6 calc_out.txt https://query1.finance.yahoo.com/v8/finance/chart/TQQQ |
| QLD 가운데 -4.5% · 손실 76% | -4.5 · 76 | S1·S6 calc_out.txt https://query1.finance.yahoo.com/v8/finance/chart/QLD |
| ±1% 76번 전부 손실 · 가운데 -13.3% | 76/76 · -13.3 | S1·S6 calc_out.txt https://query1.finance.yahoo.com/v8/finance/chart/TQQQ |
| +20% 넘은 경우 QQQ 29.8% · TQQQ 89.9% | 29.8 · 89.9 | S1·S6 calc_out.txt https://query1.finance.yahoo.com/v8/finance/chart/QQQ |
| 2021 고점 뒤 QQQ -35.1% · QLD -63.7% · TQQQ -81.7% | 같음 | S1·S6 calc_out.txt https://query1.finance.yahoo.com/v8/finance/chart/QLD |
| QQQ 716일 · 그날 TQQQ -44.0% · TQQQ 1,111일 · QLD 917일 | 같음 | S1·S6 calc_out.txt https://query1.finance.yahoo.com/v8/finance/chart/TQQQ |
| 1억 → QQQ 약 17억 · TQQQ 약 225억 (11/24 종가) | 16.9 · 225.1 | S1·S6 calc_out.txt https://query1.finance.yahoo.com/v8/finance/chart/QQQ |
| 올해 고점 대비 QQQ -16.0% · TQQQ -46.8% (11/24 종가) | 같음 | S1·S6 calc_out.txt https://query1.finance.yahoo.com/v8/finance/chart/TQQQ |
| QLD 상장 뒤 20년 · TQQQ 16년 | 2006-06-19 · 2010-02-09 상장 | S2 https://www.proshares.com/our-etfs/leveraged-and-inverse/qld · S3 https://www.proshares.com/our-etfs/leveraged-and-inverse/tqqq |
| 하루 2배·3배 · 하루보다 오래면 높거나 낮을 수 · 오르내림 크면 나빠짐 | 2x/3x daily · higher or lower · higher index volatility … worse | S2 https://www.proshares.com/our-etfs/leveraged-and-inverse/qld · S3 https://www.proshares.com/our-etfs/leveraged-and-inverse/tqqq |
| 예시 100→110→99 · 3배 130→91 (지수 -1%·3배 -9%) | 100×1.1×0.9=99 · 100×1.3×0.7=91 | 직접 산수 · S3 원리 https://www.proshares.com/our-etfs/leveraged-and-inverse/tqqq |
| 순보수 QLD 0.89% · TQQQ 0.78% | Net Expense Ratio 0.89% · 0.78% | S2 https://www.proshares.com/our-etfs/leveraged-and-inverse/qld · S3 https://www.proshares.com/our-etfs/leveraged-and-inverse/tqqq |
| 사전교육 · 기본예탁금 1천만원 · 신용·미수 막힘 | 기본예탁금(1천만원) · 사전교육 이수 · 신용·미수거래가 제한 | S4 https://www.korea.kr/briefing/actuallyView.do?newsId=148967174 |
| 상위 8편 모두 2주 전 이후 글 | 11/23 두 편·1일 전 두 편·1주 전·2주 전 세 편 | toprank.txt https://blog.naver.com/flyfreedom29/224486541790 |

# 올리기 전 확인
- 2026-11-25 15:2x firemap-write(발행 날, 칸 11/25 16:10) — 야후 QQQ·QLD·TQQQ 다시 받아 calc.py 다시, 바뀐 숫자 본문·그림·사실표 갱신·재서명
- 다시 연 주소: https://query1.finance.yahoo.com/v8/finance/chart/QQQ · https://query1.finance.yahoo.com/v8/finance/chart/QLD · https://query1.finance.yahoo.com/v8/finance/chart/TQQQ (11/25 15:26 받음) · 프로셰어즈·금융위 주소(https://www.proshares.com/our-etfs/leveraged-and-inverse/qld · https://www.proshares.com/our-etfs/leveraged-and-inverse/tqqq · https://www.korea.kr/briefing/actuallyView.do?newsId=148967174 · https://www.fsc.go.kr/po010102/87403)는 배수·보수·사전교육 문구라 가격과 무관, 11/23 확인 그대로
- 기준일: 2026-11-24 종가(미국)
- 바뀐 것: 기준일 11/20→11/24 · 2026년 QQQ -0.6%→+4.2%·QLD -9.7%→-1.8%·TQQQ -21.4%→-11.9% · 올해 고점 대비 QQQ -19.9%→-16.0%·TQQQ -52.6%→-46.8% · 1억 QQQ 약 16억→17억·TQQQ 약 201억→225억 · 1년 시작일 3,969→3,971(제자리 370·손실 91% 그대로) · 첫 문장 '거의 그대로'→'조금 올랐는데'
- 새로 찾은 것: 11/21~11/24 사이 QQQ 608.45→638.1(+4.9%), 지수가 오른 사흘에도 TQQQ 2026년 수익은 마이너스로 남음
- 조사 뒤 공표: data/release_calendar.json — 가격 매일, QLD·TQQQ 분기 분배(12월)
