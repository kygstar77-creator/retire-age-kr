# dgro1125 자료조사 (카페 11/25 18:40 배당 칸, firemap-write 11/23 21:10 회차) — DGRO 분기 배당 1년 전 대비·배당일

## 검증
- 수요: kwvol 11/23 — DGRO 2,290 · SPYD 440 · HDV 290 · NOBL 170 · 배당ETF추천 160 · 배당귀족 70. 범위 안 배당 ETF 중 아직 안 쓴 것 1위가 DGRO(VIG 1,510보다 큼)
- 사람들이 치는 말(stockwants 11/23): dgro 배당금 · 배당일 · 배당률 · 배당성장률 · 구성종목 · dgro schd 비교 · dgrw
- 경쟁에서 터진 증거: toprank 'DGRO 배당' 상위 8편 중 6편이 3주 안 글(11/23) — 관심이 몰림. 분기 배당을 1년 전 같은 분기와 하나씩 비교한 글은 상위 8편에 없음
- 겹침: 같은 날 12:40 vig1125(VIG vs VYM 10년 계산형) — 이 글은 DGRO 단독·분기 배당 기록(통계·기록형 form 4)으로 각도·꼴을 달리함. 최근 2주 카페에 DGRO 글 없음

## 원문
- S1 아이셰어즈 DGRO 상품 페이지(11/23 받음, raw/ish_page) — 설정일·총보수·지수·종목 수·업종·배당 기록: https://www.ishares.com/us/products/264623/ishares-core-dividend-growth-etf
- S2 아이셰어즈 2026-2028 배당 일정표(11/18자, raw/ish_sched.pdf 4쪽 DGRO 묶음): https://www.ishares.com/us/literature/shareholder-letters/isharesandblackrocketfsdistributionschedule.pdf
- S3 야후 파이낸스 chart API DGRO·SCHD·VIG·SPY 일별 종가·배당 events(11/23 받음, raw/*.json, fetch.py): https://query1.finance.yahoo.com/v8/finance/chart/DGRO
- S4 S3로 직접 계산(calc.py → calc_out.txt). 2025-09~2026-09 배당 5번은 S1 금액과 대조(0.369·0.447·0.331·0.331·0.385 일치)

## 경쟁
- toprank.txt('DGRO 배당' 블로그 상위 8, 11/23) — 1위 royal23- VIG·DGRO 배당률·수익률 비교, 2위 cndtlr1221 SCHD+DGRO 5:5, 3위 real_bin 월 50만원 필요 금액, 4위 okor22 선정 기준·SCHD·VIG 차이, 5위 neighbormrbear 배당일·배당성장률·구성종목, 6위 real_bin DGRO vs DGRW
- 빠뜨린 것: 분기 배당이 1년 전보다 줄었던 때(5위는 2025년 연간 성장률만), 가장 많이 준 달이 9월이 더 잦았다는 기록

## 질문
1. DGRO 배당금은 언제 얼마 나오나 — https://blog.naver.com/neighbormrbear/224450259236 ('DGRO ETF 배당일과 배당성장률') → 답: 3·6·9·12월, 올해 0.331·0.331·0.385달러, 12월 15일 배당락·18일 지급
2. DGRO 배당은 꾸준히 늘었나(배당성장률) — https://blog.naver.com/okor22/224477925389 ('5년 이상 배당 성장주만 골라 담는 DGRO') → 답: 1년 합은 2017~2025 해마다 늘어 2.06배, 분기로는 38번 중 4번 감소
3. DGRO와 SCHD 중 뭐가 나은가 — https://blog.naver.com/cndtlr1221/224477138740 ('SCHD와 찰떡궁합 DGRO 5:5 포트폴리오') → 답: 지금 배당률은 SCHD 3.1% vs DGRO 1.9%, 11년 배당 재투자 결과는 3만 7,800 vs 3만 7,500달러로 비슷
4. 12월 배당이 가장 큰가 — https://blog.naver.com/real_bin/224465288342 ('DGRO 분배금과 배당수익률') → 답: 9년 중 9월 5번·12월 4번

## 왜
- 왜 배당률이 SCHD보다 낮나: 원문(S1)은 '배당을 늘려 온 미국 주식을 모은 지수'라고만 적음 — 정보기술 17%(S1)는 사실로만 씀, 원인으로 안 씀
- 왜 분기 배당이 줄었나: 원문(S1·S2)에 이유 없음 — 글에 '자료에 따로 적혀 있지 않다'고 씀

## 그래서
- 분기마다 일정한 돈이 필요하면 1년 전보다 적은 분기가 있을 수 있다는 점을 계산에 넣는다(38번 중 4번)
- 12월 배당을 받으려면 12월 15일(미국) 전 거래일까지 보유 — 금액은 12월 14일 발표(S2)

## 누구라면
- 분기 배당으로 생활비를 쓰는 사람: 지금 배당률 1.9%, 분기 금액이 1년 전보다 적었던 때가 4번
- 오래 모을 사람: 11년(2015-11-20~2026-11-20) 배당 재투자 1만 달러 → 약 3만 7,800달러(SCHD·VIG와 비슷, SPY보다 적음)
- 하락이 무서운 사람: 2021년 이후 최대 낙폭 DGRO 19.3% · SCHD 16.8% · VIG 20.4%

## 함정
- '12월 배당이 늘 가장 크다'는 말 — 9년 중 4번뿐
- '배당성장 ETF니까 분기 배당도 매번 는다'는 생각 — 1년 합은 늘었지만 분기는 4번 줄었음

## 한계
- 달러 기준·세전 — 환율·미국 원천징수·국내 세금은 안 넣음
- 야후 2016년 기록은 3번뿐이라 1년 합은 2017년부터 셈, 2016년 3월 배당은 확인 못 함
- 모닝스타 지수 방법론 PDF가 안 열려 종목 고르는 기준(5년 연속·배당성향 등)은 글에 안 씀
- 구성종목 상위 목록은 아이셰어즈 내려받기 파일이 안 받아져 업종 비중만 씀
- 2026년 12월 금액은 미발표

## 대조
| 글 값 | 원문 값 | 출처 |
|---|---|---|
| 2014년 6월 설정 · 총보수 0.08% · 390개 · 금융 19%·헬스케어·정보기술 17%씩 | 2014-06-10 · 0.08% · 390(11/20) · 19.35·17.47·17.05%(11/19) | S1 https://www.ishares.com/us/products/264623/ishares-core-dividend-growth-etf |
| 올해 3월 0.331·6월 0.331·9월 0.385달러, 작년 12월 0.447달러 | 0.331063 · 0.330603 · 0.384996 · 0.447036 | S1 https://www.ishares.com/us/products/264623/ishares-core-dividend-growth-etf |
| 12월 14일 발표·15일 배당락·18일 지급 | 14-Dec-26 · 15-Dec-26 · 18-Dec-26 | S2 https://www.ishares.com/us/literature/shareholder-letters/isharesandblackrocketfsdistributionschedule.pdf |
| 지금 배당률 DGRO 1.9%·SCHD 3.1%·VIG 1.5%대 | 1.93 · 3.11 · 1.55(최근 12달 배당 ÷ 11/20 종가) | S3·S4 https://query1.finance.yahoo.com/v8/finance/chart/DGRO |
| 38번 중 4번 감소 · 2017-09 0.165(0.175) · 2021-09 0.250(0.261) · 2022-06 0.235(0.261) · 2025-09 0.369(0.403) | 같음 | S3·S4 https://query1.finance.yahoo.com/v8/finance/chart/DGRO |
| 1년 배당 0.706→1.451달러, 2배 조금 넘게·해마다 9% 정도 | 2.06배 · 9.4% | S3·S4 https://query1.finance.yahoo.com/v8/finance/chart/DGRO |
| 가장 많이 준 달 9월 5번·12월 4번 | 같음 | S3·S4 https://query1.finance.yahoo.com/v8/finance/chart/DGRO |
| 1~3분기 합 1.047달러, 작년보다 4% 정도 | 1.047 vs 1.004(+4.3%) | S3·S4 https://query1.finance.yahoo.com/v8/finance/chart/DGRO |
| 1만 달러 → 약 3만 7,800·3만 7,500·3만 6,800·3만 9,400달러 | 37,828 · 37,511 · 36,823 · 39,422 | S3·S4 https://query1.finance.yahoo.com/v8/finance/chart/SPY |
| 최대 낙폭 19.3%·16.8%·20.4% | -19.3 · -16.8 · -20.4 | S3·S4 https://query1.finance.yahoo.com/v8/finance/chart/SCHD |

# 올리기 전 확인
- 2026-11-23 21:2x 작성 시 S1·S2·S3 다시 받음. 발행 회차(11/25)가 다시 열어 적을 것
기준일: 2026-11-20 미국 종가
바뀐 것: 없음(작성일)
새로 찾은 것: 아이셰어즈 일정표 11/18자 4분기 12/15 배당락
