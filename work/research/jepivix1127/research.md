# jepivix1127 자료조사 (카페 11/27 12:40 배당 칸, firemap-write 11/25 23:1x 회차) — JEPI 분배금과 앞 달 VIX, 77번 직접 계산

## 검증
- 수요: kwvol 11/25 — JEPI 8,070 · 고배당ETF 3,820 · 월배당ETF 2,850 · JEPIETF 1,410 · VYM 450 · 배당귀족 70
- 경쟁에서 터진 증거: toprank 'JEPI 분배금' 상위 8편 전부 3주 안 글, 5위 '왜 매달 분배금이 달라질까?', 7위는 '변동성이 커지면 분배금이 늘어나는지'를 앞으로 볼 것으로 남김(세지 않음)
- 겹침: 지난 30일 카페에 JEPI 단독 글 없음(#456 JEPQ 1억·#471 QQQI 주가·#470 DIVO 12월) — 11/26 decdiv1126에 JEPI 12월 배당락 한 줄은 있으나 VIX 관계는 안 다룸
- 칸: 11/27 12:40 배당(slots.json TBD 배당, 관문 기한 11/27 06:40) · 10:10 dow1124 지수·16:10 TBD 지수 사이

## 원문
- S1 야후 파이낸스 chart API JEPI·SPY·^VIX 일별 종가·분배 events, 11/25 23:3x 받음(raw/*.json, fetch.py): https://query1.finance.yahoo.com/v8/finance/chart/JEPI
- S2 미국 증권거래위원회(SEC) JEPI 요약 투자설명서 497K(2026-10-20) — ELN 20%·콜옵션 프리미엄·상승 제한·총보수 0.35%: https://www.sec.gov/Archives/edgar/data/1485894/000119312526425888/d380375d497k.htm (raw/sec_000119312526425888.htm)
- S3 Cboe VIX 소개 — S&P500 옵션 가격에 담긴 단기 변동성 기대: https://www.cboe.com/tradable_products/vix/
- S4 Cboe 인사이트 11/9 주간(11/5 급등·11/9 19.92): https://www.cboe.com/insights/posts/week-of-11-9-2026-no-contagion-yet-equity-vol-spikes-macro-vol-fades
- S5 S1으로 직접 계산(calc.py → calc_out.txt), 기준일 2026-11-24 종가(11/25 장중 값 뺌)

## 경쟁
- toprank.txt('JEPI 분배금' 블로그 상위 8, 11/25) — 1위 투자 전 체크리스트, 2위 월 50만원이면 몇 주, 4위 12월 언제·얼마, 5위 왜 매달 다를까(최근 6개월 표), 7위 하락장 총수익(변동성-분배금은 '앞으로 볼 것'), 8위 SPYI·JEPI·QQQI 비교
- 247월스트 6/17 '분배가 달마다 흔들린다'·5/28 '변동성 함정' — VIX와 분배금 관계를 말로만, 묶어 센 표 없음
- 앞 달 VIX로 77번을 묶어 센 글은 상위 8편·해외 2편에 없음

## 질문
1. JEPI 분배금은 왜 매달 다를까 — https://blog.naver.com/quf02071227/224468940303 ('JEPI 배당금 왜 매달 분배금이 달라질까?') → 답: 옵션 판 돈이 재료라 앞 달 VIX가 높을수록 컸음(10.3% vs 7.1%)
2. 변동성이 커지면 분배금이 늘어나나 — https://blog.naver.com/coldbull_iy/224491551500 ('변동성이 커지면 콜옵션 값이 올라 분배금이 늘어나는지') → 답: 대체로 그랬음, 29번 중 5번은 예외
3. 12월 분배금은 얼마나 될까 — https://blog.naver.com/mijangdad/224491239615 ('JEPI 월배당, 12월엔 언제 들어오고 얼마나 될까') → 답: 발표 전, 과거엔 12월 배당락 두 번
4. 분배율 8%가 안정적인가 — https://247wallst.com/investing/2026/06/17/jepis-8-2-percent-yield-looks-safe-until-you-see-how-the-distribution-swings-month-to-month/ ('Looks Safe Until You See How the Distribution Swings') → 답: 1년 환산 5.0~13.4%로 흔들림

## 왜
- 왜 VIX가 높으면 분배금이 커지나: JEPI 수익의 중요한 재료가 ELN 안 S&P500 콜옵션 매도 프리미엄(S2)이고, VIX는 그 S&P500 옵션 가격에서 나온 지수(S3) — VIX가 높으면 같은 옵션을 더 비싸게 판다
- 왜 VIX 높은데 낮았던 달이 있나(2021-02 등): 원문(S2)에 이유 없음 — 없다고 적음
- 왜 총수익이 SPY보다 낮나: 콜옵션을 팔면 오를 때 이익이 행사가까지로 제한(S2)

## 그래서
- 분배금으로 생활비를 쓰면 VIX가 낮은 해(2024 1주 4.22달러)를 기준으로 잡는 편이 덜 흔들린다 — 높은 해(2022 6.36)를 기준으로 잡으면 모자라는 달이 생김
- 12월 분배금은 발표 전 — 지난 기록으로 금액을 미리 정하지 않는다

## 누구라면
- 은퇴 뒤 매달 분배금으로 생활비 쓰는 사람: 같은 1주라도 0.26~0.62달러로 흔들림, 낮은 달 기준으로 계획
- 오래 모을 사람: 상장 뒤 분배 재투자 1.9배 vs SPY 2.7배
- 하락이 무서운 사람: 2022년 주가 JEPI -13.4% vs SPY -19.9%

## 함정
- '변동성 크면 분배금 늘어난다' = 대체로 맞지만 29번 중 5번 예외
- 분배금 많은 때 = 주가 빠지는 때(2022) — 분배금만 보면 손익을 놓침
- 12월 배당락 두 번이라 12월 합이 커 보임(1월 없음)

## 한계
- 앞 달 VIX 평균과 묶은 것은 우리 기준(옵션 만기·매도 시점은 원문에 달마다 안 나옴)
- 달러·세전 — 미국 원천징수·국내 세금·환율 안 넣음
- 2020-05 상장이라 6년 반 77번뿐, 2008 같은 큰 하락장 기록 없음
- 분배 기록은 야후로 셈 — JP모건 미국 홈페이지 분배 표는 동적 화면이라 못 열었고, 경쟁 글 2편(quf02071227·mijangdad)이 운용사 기준으로 적은 11월 0.34683·10월 0.34134·5월 0.44761·12개월 합 4.56417과 야후 값이 같음(2차 대조)
- 국내 상장 커버드콜 ETF는 안 셈

## 대조
| 글 값 | 원문 값 | 출처 |
|---|---|---|
| 11월 20일 VIX 35.89 · 11/4 16.61 → 11/5 28.18 | 35.89 · 16.61 · 28.18 | S1 https://query1.finance.yahoo.com/v8/finance/chart/%5EVIX · S4 |
| 2020년 7월 이후 77번 | 77(첫 2020-07-01) | S1 https://query1.finance.yahoo.com/v8/finance/chart/JEPI |
| 앞 달 VIX 20 이상 10.3%(29번)·15~20 7.7%(38번)·15 미만 7.1%(10번) | 10.34 · 7.67 · 7.07 | S1·S5 calc_out.txt https://query1.finance.yahoo.com/v8/finance/chart/JEPI |
| 1주당 가운데 값 0.48·0.34달러 | 0.481 · 0.338 | S1·S5 https://query1.finance.yahoo.com/v8/finance/chart/JEPI |
| 2022년 VIX 25.6·분배 6.36달러 / 2024년 15.6·4.22달러 | 25.6 · 6.361 / 15.6 · 4.216 | S1·S5 https://query1.finance.yahoo.com/v8/finance/chart/JEPI |
| 2021년 2월 앞 달 VIX 24.9·5.8% 꼴, 두 번째로 낮음 | 24.9 · 5.75(최저 2021-08 5.00) | S1·S5 https://query1.finance.yahoo.com/v8/finance/chart/JEPI |
| 29번 중 5번이 가운데 값 7.9%보다 낮음 | 5 · 7.93 | S1·S5 https://query1.finance.yahoo.com/v8/finance/chart/JEPI |
| 올해 3월 VIX 25.6(올해 최고)·4월 0.42달러 / 9월 15.8·10월 0.34달러 | 25.6 · 0.421 / 15.8 · 0.341 | S1·S5 https://query1.finance.yahoo.com/v8/finance/chart/JEPI |
| 2022년 주가 JEPI -13.4%·SPY -19.9% | -13.4 · -19.9 | S1·S5 https://query1.finance.yahoo.com/v8/finance/chart/SPY |
| 1만 달러 → 분배 약 6,200·평가액 약 1만 1,200달러 | 6,223 · 11,221 | S1·S5 https://query1.finance.yahoo.com/v8/finance/chart/JEPI |
| 분배 재투자 JEPI 약 1.9배·SPY 약 2.7배 | 1.944 · 2.665 | S1·S5 https://query1.finance.yahoo.com/v8/finance/chart/SPY |
| 2020년 5월 출시·총보수 0.35%·ELN 20%·콜옵션 프리미엄이 중요한 재료·오를 때 몫 포기 | Total Annual Fund Operating Expenses 0.35 · up to 20% in ELNs · important source of the Fund's return · limits its opportunity to profit | S2 https://www.sec.gov/Archives/edgar/data/1485894/000119312526425888/d380375d497k.htm |
| VIX = S&P500 옵션 가격에서 뽑은 지수 | expectations of near-term volatility conveyed by S&P 500 Index option prices | S3 https://www.cboe.com/tradable_products/vix/ |
| 12월 배당락 두 번(2020~2025), 1월 없음 | 12-01·12-30 / 12-01·12-30 / 12-01·12-29 / 12-01·12-28 / 12-02·12-31 / 12-01·12-31 | S1 https://query1.finance.yahoo.com/v8/finance/chart/JEPI |

# 올리기 전 확인
- 2026-11-26 00:0x firemap-write(작성 회차, 발행 하루 반 전) — 야후 JEPI·SPY·^VIX 11/25 23:3x 받아 계산, 기준일 2026-11-24 종가
- 다시 연 주소: https://query1.finance.yahoo.com/v8/finance/chart/JEPI (11/25) · https://query1.finance.yahoo.com/v8/finance/chart/SPY (11/25) · https://query1.finance.yahoo.com/v8/finance/chart/%5EVIX (11/25) · https://www.sec.gov/Archives/edgar/data/1485894/000119312526425888/d380375d497k.htm (11/25) · https://www.cboe.com/tradable_products/vix/ (11/25) · https://www.cboe.com/insights/posts/week-of-11-9-2026-no-contagion-yet-equity-vol-spikes-macro-vol-fades (11/25)
- 기준일: 2026-11-24 미국 종가
- 바뀐 것: 처음 작성 — 바뀐 값 없음. 발행 회차(11/27 12:10)에 fetch.py·calc.py·mkimg.py 다시 돌려 11/26 종가로 갱신, 12월 분배 금액이 발표돼 있으면 c05 '발표 전' 줄 고침
- 새로 찾은 것: 11월 VIX 평균 23.4(11/24까지)로 올해 3월 25.6 다음 — 11/25 장중 31.7은 종가가 아니라 안 씀
- 조사 뒤 공표: data/release_calendar.json — JEPI 12월 분배 금액 발표(12/1 배당락 전) → 발행 회차에서 확인
- 2026-11-27 10:4x firemap-write-b(발행 날, 12:40 칸) — fetch.py·calc.py·mkimg.py 다시 돌림
- 다시 연 주소: https://query1.finance.yahoo.com/v8/finance/chart/JEPI (11/27) · https://query1.finance.yahoo.com/v8/finance/chart/SPY (11/27) · https://query1.finance.yahoo.com/v8/finance/chart/%5EVIX (11/27) · https://www.sec.gov/Archives/edgar/data/1485894/000119312526425888/d380375d497k.htm (11/27) · https://www.cboe.com/tradable_products/vix/ (11/27) · https://www.cboe.com/insights/posts/week-of-11-9-2026-no-contagion-yet-equity-vol-spikes-macro-vol-fades (11/27) · https://ycharts.com/companies/JEPI/dividend (11/27)
- 기준일: 2026-11-25 미국 종가(11/26 추수감사절 휴장)
- 바뀐 것: 기준일 11/24→11/25 · 재투자 평가액 JEPI 19,440→19,451달러(약 1만 9,400→1만 9,500)·SPY 26,650→26,574달러(약 2만 6,700→2만 6,600) · 11월 VIX 평균 23.4→23.7(본문엔 안 씀) · 분배 77번·묶음 중간값 10.3%·7.7%·7.1%·예외 5번·1.9배·2.7배 그대로 · c04·c05('11월 27일 현재')·c06 기준일, 그림 3장 날짜 줄 고침
- 새로 찾은 것: JEPI 12월 분배 금액 11/27 현재 미발표(ycharts 마지막 11/2 0.3468달러) — c05 '발표 전' 줄 유지
- 조사 뒤 공표: JEPI 12월 분배 금액 발표(12/1 배당락 전 예상) — 발행 뒤라 이 글엔 안 들어감
