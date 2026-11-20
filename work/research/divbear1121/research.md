# divbear1121 자료조사 (카페 11/21 22:40 배당 칸 — 쇼츠 de1s_drop2022 mOrYhIcsQ40 짝 글, firemap-write-b 11/20 13:40 회차) — 배당 ETF, 직접 계산형

## 검증
- 수요: 쇼츠 짝 글(사장님 10/11 '유튜브에 올린 것은 카페에도 반드시 글') · video-producer [요청] 11/19 22:50 · toprank '배당 ETF 하락장' 상위 8편 중 6편이 2주 안 글(11/20) — 지금 미국 증시 하락(SPY 최고 대비 -8.1%)과 겹침 · kwvol은 이번 회차 안 잼(확인 안 함)
- 경쟁에서 터진 증거: 상위 1(etflab_us) 'QQQ 7.9% 빠진 한 달 …' 댓글 4 · 쇼츠 경쟁 똑재TV '슈드 빠졌을 때' 2.8만 회(cardshorts/de1s_drop2022/compete.md)
- 겹침: 우리 divdrop1020('고배당 ETF는 급락한 날 덜 빠졌는데 왜 2년 반 수익은 졌을까?')은 국내 고배당 ETF·코스피 하루 3% 급락일 — 이번은 미국 배당 ETF·하락장 두 번·회복 기간이라 다름 · 11/21 칸 kdiv1121(국내 PLUS 고배당주 분배금)과도 다름
- 칸: 11/21 22:40 배당(slots.json, 관문 기한 11/21 16:40)

## 원문
- S1 야후 파이낸스 chart API 일별 가격·adjclose(배당 재투자·분할 반영) SPY·SCHD·JEPI·HDV·SPYD·402970.KS, 2019-01-01~2026-11-19, 2026-11-20 13:5x 받음(raw/*_chart_20261120.json, fetch.py): https://query1.finance.yahoo.com/v8/finance/chart/SCHD
- S2 같은 자료로 직접 계산(calc.py → calc_out.txt) — 원자료 S1
- S3 D-ETF-1 calc_out.txt(10/19, 같은 야후 자료 다른 날 받음) — 2022·2020 낙폭 숫자 같음: work/research/longform/ep/D-ETF-1/calc_out.txt
- S4 FRED FEDFUNDS 2022-01 0.08% → 2022-12 4.10%(apis.fred, 11/20 받음 raw/fred_fedfunds_2022.json): https://fred.stlouisfed.org/series/FEDFUNDS
- S5 쇼츠 https://youtu.be/mOrYhIcsQ40 (11/21 19:20 공개 예약) · 롱폼 https://youtu.be/mkAxQPGaDqc (10/30 공개)

## 경쟁
- toprank.txt('배당 ETF 하락장' 블로그 상위 8, 11/20). 1(etflab_us)은 최근 한 달 QQQ -7.88% vs 미국배당다우존스 +6.5%·국내 5종 수익률, 3(2739ksm)은 파이어족 유튜버 사례, 5(dividendwhisky)는 VYM·HDV·SPYD 구성 설명 뒤 '방어 효과는 실제 최대 낙폭과 회복 기간으로 확인해 보세요'라고만 하고 숫자 없음, 4(bini1976)는 개인 계좌 -15.5%. 하락장 두 번을 같은 잣대로 낙폭·회복 기간까지 센 글 0편 → bench.md

## 질문
1. 하락장에 배당 ETF는 정말 덜 빠지나 — https://blog.naver.com/dividendwhisky/224467744889 (제목 '고배당 ETF는 하락장에서 정말 방어적일까요?') → 답: 2022년엔 SCHD 16.8%·JEPI 13.7%로 S&P500 24.5%보다 덜, 코로나 땐 SCHD 33.4%로 시장만큼·SPYD 46.4%로 더
2. 배당 ETF는 하락 뒤 얼마 만에 회복했나 — https://youtu.be/mOrYhIcsQ40 (쇼츠 이해 시험 3차 '남은 궁금증: 회복 기간', cardshorts/de1s_drop2022/understand.md) → 답: 2022년 SCHD 14.9달·HDV 2.0달·SPYD 21.4달, 코로나 SCHD 약 5달·HDV·SPYD 11달 넘게
3. 요즘 하락장에 배당 ETF가 선방하나 — https://blog.naver.com/etflab_us/224480895309 (제목 'QQQ 7.9% 빠진 한 달, 6.5% 오른 미국배당다우존스') → 답: 11/19 종가로 SPY 최고 대비 -8.1%, SCHD -5.6%
4. 국내 상장 미국배당다우존스도 같나 — https://blog.naver.com/bini1976/224483924166 (제목 '… 총수익률 -15.5%와 SOL 미국배당다우존스') → 답: 원화라 환율이 섞임, ACE 미국배당다우존스 2022년 안 최대 낙폭 9.5%

## 왜
- 왜 배당 다시 넣은 값: 분배금을 빼면 배당 많은 ETF가 손해로 보임 — 같은 잣대로 놓으려고(본문 '놓치기 쉬운 것' 첫째)
- 왜 2022엔 덜, 코로나엔 같이: 가격 자료에 이유 칸 없음 — 2022년은 금리가 빠르게 오른 해(S4)라는 사실까지만 씀. 업종 탓이라는 설명은 경쟁 글 추정이라 안 옮김
- 왜 회복이 늦었나: 이유는 자료에 없음 — 날짜만 씀

## 그래서
- 배당 ETF를 '하락장 방패'로 들고 있다면: 2022년처럼 덜 빠진 때도 원래 값까지 15달 걸린 적이 있다는 걸 알고 버틸 기간을 잡음
- 고배당(SPYD·HDV)은 코로나처럼 급락하면 시장보다 더 빠지고 회복도 늦었음 → 상품마다 지난 낙폭을 먼저 확인
- 배당을 꺼내 쓰면 계좌 회복이 더 늦음

## 누구라면
- 배당 ETF로 생활비를 받는 은퇴자: 배당을 꺼내 쓰므로 위 숫자(재투자 기준)보다 계좌가 더 빠짐
- 국내 상장 미국배당다우존스(원화)로 모으는 사람: 환율이 섞여 달러 숫자와 다름(2022년 9.5%)
- S&P500 ETF만 가진 사람: 2022년엔 더 빠졌고, 코로나 땐 SCHD와 비슷했고 회복은 가장 빨랐음

## 함정
- '배당 ETF = 덜 빠진다'를 한 하락장만 보고 믿는 것 — 코로나 땐 SCHD도 시장만큼, SPYD는 더
- 2022 낙폭은 그해 안 고점 기준 — 2021년 말 고점과 다를 수 있음(본문에 '그해 안에서' 씀)
- 배당 꺼내 쓴 계좌는 재투자 값보다 나쁨

## 한계
- 야후 adjclose 하나로 셈 — 운용사 공식 연도별 수익은 이번에 대조 안 함(D-ETF-1 10/19 같은 자료로 같은 값)
- 세금(배당 15%)·수수료·환전비 뺌
- 하락장 두 번뿐 — 다른 하락장(2008 등)은 SCHD·JEPI·SPYD 상장 전이라 못 봄
- JEPI 코로나 기록 없음(2020-05-21 상장)
- 지금 하락은 진행 중이라 바닥·회복은 모름

## 대조
| 글 값 | 원문 값 | 출처 |
|---|---|---|
| 2022년 고점에서 SPY 24.5%·SCHD 16.8% 빠짐 | -24.5(2022-01-03→10-12) · -16.8(01-11→09-30) | S1·S2 calc_out.txt, S3 |
| JEPI 13.7%·HDV 15.4%·SPYD 20.3% | -13.7 · -15.4 · -20.3 | S1·S2 calc_out.txt, S3 |
| 2022년 한 해 SPY 18.2% 잃음·SCHD 3.3%·HDV 7.0% 벎 | -18.2 · -3.3 · +7.0 | S1·S2 calc_out.txt |
| 코로나 SPY 33.7%·SCHD 33.4% | -33.7(02-19→03-23) · -33.4(01-23→03-23) | S1·S2 calc_out.txt, S3 |
| HDV 37.0%·SPYD 46.4% | -37.0 · -46.4 | S1·S2 calc_out.txt, S3 |
| SPYD 1천만원 → 두 달 만에 약 536만원 | 1,000×0.536 · 01-16→03-23 | S1·S2 calc_out.txt |
| JEPI 2020년 5월에 나옴 | firstTradeDate 2020-05-21 | S1 raw/JEPI_chart_20261120.json |
| 2022 회복 SPY 14.0달(2023-12-13)·SCHD 14.9달(2023-12-28) | 14.0달 · 14.9달 | S1·S2 calc_out.txt |
| JEPI 8.5달(2023-06-15)·HDV 2.0달(2022-11-30)·SPYD 21.4달(2024-07-11) | 8.5 · 2.0 · 21.4달 | S1·S2 calc_out.txt |
| 코로나 회복 SPY 4.6달·SCHD 5.4달·HDV 11.5달·SPYD 11.1달 | 4.6 · 5.4 · 11.5 · 11.1달 | S1·S2 calc_out.txt |
| SCHD가 SPY보다 보름 늦게 | 12-13 → 12-28, 15일 | S1·S2 calc_out.txt |
| ACE 미국배당다우존스 2022년 안 9.5%·두 달 안 돼 고점 되찾음 | -9.5(01-07→02-24) · 회복 04-20 | S1·S2 calc_out.txt |
| 11/19 SPY 최고점보다 8.1%·SCHD 5.6% 아래 | -8.1(최고 10-06) · -5.6(최고 11-04) | S1·S2 calc_out.txt |
| 2022년 미국 금리 빠르게 오름 | FEDFUNDS 0.08 → 4.10 | S4 https://fred.stlouisfed.org/series/FEDFUNDS |

# 올리기 전 확인
- 2026-11-20 14:2x firemap-write-b(조사·작성 날, 발행 날 11/21 22:40 write-b 회차가 야후 다시 받아 '지금' 줄(11/20·21 종가) 갱신)
- 다시 연 주소: https://query1.finance.yahoo.com/v8/finance/chart/SCHD (SPY·JEPI·HDV·SPYD·402970.KS 같은 꼴, 11/20 13:5x 받음) · https://fred.stlouisfed.org/series/FEDFUNDS (apis.fred 11/20) · work/research/longform/ep/D-ETF-1/calc_out.txt(11/20 다시 엶) · https://youtu.be/mkAxQPGaDqc (공개)
- 기준일: 야후 2026-11-19 종가(11/20 조회) · FRED 2022년 월값
- 바뀐 것: 처음 조사 — 없음
- 새로 찾은 것: 바닥 뒤 회복 기간(2022 SCHD 14.9달·HDV 2.0달·SPYD 21.4달, 코로나 SCHD 5.4달·SPYD 11.1달) · 국내 ACE 미국배당다우존스 2022 낙폭 -9.5% · 지금 SPY -8.1%·SCHD -5.6% · 경쟁 글 회복 기간 센 글 0편
- 조사 뒤 공표: data/release_calendar.json — 가격은 매일, 발행 날 다시 받아 '지금' 줄 갱신
